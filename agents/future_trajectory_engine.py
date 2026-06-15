"""Future Trajectory Engine for NERVA Resonance

This module produces explainable alternative future-state projections
for enterprise decisions. It is intentionally conservative, auditable,
and designed for integration with the NERVA multi-agent stack.

Primary outputs (per decision):
 - Best Case Future
 - Expected Future
 - Worst Case Future

Each projection includes:
 - confidence_score: float in [0.0, 1.0]
 - risk_score: float (higher means more risk)
 - reasoning_chain: List[str] explaining how the projection was derived
 - recommended_action: List[str] of actions to take
 - projected_outcomes: Dict[str, Any] describing likely outcomes

Integration:
 - Consumes `ConsequenceResult` produced by `agents.consequence_cascade`.
 - Usable by `agents/reasoning_agent.py` and NERVA Resonance simulators.

Example usage:

    from agents.consequence_cascade import ConsequenceCascadeEngine
    from agents.future_trajectory_engine import FutureTrajectoryEngine

    cascade = ConsequenceCascadeEngine()
    result = cascade.assess_decision("Delay shipment by 48h", context={"order_id": "ORD-1"})

    engine = FutureTrajectoryEngine()
    projections = engine.generate_projections(decision_summary="Delay shipment by 48h", cascade_result=result)
    print(projections)

"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import math
import logging

try:
    # integration with existing consequence cascade datatypes
    from agents.consequence_cascade import ConsequenceResult, ImpactAssessment
except Exception:  # pragma: no cover - defensive fallback for import errors
    ConsequenceResult = Any  # type: ignore
    ImpactAssessment = Any  # type: ignore

logger = logging.getLogger(__name__)


@dataclass
class FutureScenario:
    """Represents configuration for a future scenario.

    Attributes:
        name: short label for the scenario (e.g., 'Best Case').
        multiplier: risk multiplier applied to the base cascade (<=1 for optimistic).
        description: human-readable description of the scenario assumptions.
    """

    name: str
    multiplier: float = 1.0
    description: str = ""


@dataclass
class FutureProjection:
    """Dataclass representing a single future projection.

    Fields are chosen for JSON-serializability and enterprise diagnostics.
    """

    scenario: str
    confidence_score: float
    risk_score: float
    reasoning_chain: List[str]
    recommended_action: List[str]
    projected_outcomes: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation of the projection."""
        return asdict(self)


class FutureTrajectoryEngine:
    """Engine that synthesizes explainable future trajectories from
    a `ConsequenceResult` produced by `agents.consequence_cascade`.

    Usage patterns:
      - Called by `reasoning_agent` after obtaining a consequence cascade.
      - Ingested by `NERVA Resonance` for simulation/visualization.

    The engine does not attempt black-box forecasting. Instead it applies
    transparent heuristics (multipliers, aggregation, and reasoning synthesis)
    to produce three alternative projections.
    """

    def __init__(self, resonance_adapter: Optional[Any] = None, shared_context: Optional[Dict[str, Any]] = None) -> None:
        self.resonance_adapter = resonance_adapter
        self.shared_context = shared_context or {}

    def generate_projections(self, decision_summary: str, cascade_result: Optional[Union[ConsequenceResult, Dict[str, Any]]] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
        """Generate best/expected/worst projections.

        Args:
            decision_summary: Natural language summary of the decision.
            cascade_result: Output from `ConsequenceCascadeEngine.assess_decision()`.
            context: Optional extra context (e.g., enterprise context, simulation flags).

        Returns:
            A mapping with keys `best_case`, `expected`, `worst_case`, each
            containing a JSON-serializable `FutureProjection` dict.
        """
        context = context or {}

        # Accept either dataclass-style ConsequenceResult or plain dict
        cr = cascade_result

        # Base aggregation from cascade_result
        base_confidence = 0.0
        base_risk = 0.0
        assessments: List[ImpactAssessment] = []
        recommended_actions: List[str] = []

        if cr is None:
            logger.debug("No cascade_result provided; generating neutral defaults")
        else:
            if hasattr(cr, "assessments"):
                assessments = list(getattr(cr, "assessments"))
                base_confidence = float(getattr(cr, "overall_confidence", 0.0))
                base_risk = float(getattr(cr, "overall_risk_score", 0.0))
                recommended_actions = list(getattr(cr, "recommended_actions", []) or [])
            elif isinstance(cr, dict):
                assessments = cr.get("assessments", [])
                base_confidence = float(cr.get("overall_confidence", 0.0))
                base_risk = float(cr.get("overall_risk_score", 0.0))
                recommended_actions = cr.get("recommended_actions", [])

        # Define scenarios
        scenarios = [
            FutureScenario(name="Best Case", multiplier=0.65, description="Optimistic mitigation and favorable external conditions."),
            FutureScenario(name="Expected", multiplier=1.0, description="Most-likely continuation of current signals."),
            FutureScenario(name="Worst Case", multiplier=1.45, description="Adverse cascade, compounding failures, and degraded mitigations."),
        ]

        projections: Dict[str, FutureProjection] = {}

        for s in scenarios:
            conf = self._score_confidence(base_confidence, s.multiplier, assessments, context)
            risk = self._score_risk(base_risk, s.multiplier, assessments, context)
            reasoning = self._synthesize_reasoning(decision_summary, s, assessments, context)
            actions = self._synthesize_recommendations(recommended_actions, s, assessments, context)
            outcomes = self._project_outcomes(decision_summary, s, assessments, context, base_risk)

            proj = FutureProjection(
                scenario=s.name,
                confidence_score=round(conf, 4),
                risk_score=round(risk, 4),
                reasoning_chain=reasoning,
                recommended_action=actions,
                projected_outcomes=outcomes,
            )

            key = s.name.lower().replace(" ", "_")
            projections[key] = proj.to_dict()

        # Optionally send to resonance adapter for simulation ingestion
        try:
            if self.resonance_adapter and hasattr(self.resonance_adapter, "ingest_projection"):
                self.resonance_adapter.ingest_projection({"decision": decision_summary, "projections": projections, "context": self.shared_context})
        except Exception:
            logger.exception("Failed to send projections to resonance_adapter")

        return projections

    # -- Heuristic helpers -------------------------------------------------
    def _score_confidence(self, base_confidence: float, multiplier: float, assessments: List[ImpactAssessment], context: Dict[str, Any]) -> float:
        """Derive a scenario confidence score.

        The best case increases confidence modestly; worst case reduces it.
        Confidence is clamped to [0.0, 1.0].
        """
        conf = base_confidence if base_confidence else 0.6
        # heuristics: optimistic scenario slightly increases confidence
        conf = conf * (1.0 + (1.0 - multiplier) * 0.25)
        # penalize when assessments contain high-uncertainty items
        uncertainty = 0.0
        for a in assessments:
            try:
                uncertainty += max(0.0, 0.5 - float(getattr(a, "confidence", 0.5)))
            except Exception:
                continue
        if uncertainty > 0:
            conf -= min(0.2, uncertainty * 0.05)
        return max(0.0, min(1.0, conf))

    def _score_risk(self, base_risk: float, multiplier: float, assessments: List[ImpactAssessment], context: Dict[str, Any]) -> float:
        """Compute a scenario risk score using multiplier and assessment signals.

        The function blends the supplied `base_risk` with per-horizon risk
        accumulation so results remain explainable.
        """
        risk = base_risk if base_risk else 0.0
        # derive an additive term from high-severity assessments
        add = 0.0
        for a in assessments:
            try:
                sev = float(getattr(a, "severity", 0.0))
                lik = float(getattr(a, "likelihood", 0.0))
                add += (sev * lik) * (1.0 + (1.0 - float(getattr(a, "confidence", 0.5))))
            except Exception:
                continue
        # Apply scenario multiplier and diminishing returns
        combined = (risk + add) * multiplier
        return combined

    def _synthesize_reasoning(self, decision_summary: str, scenario: FutureScenario, assessments: List[ImpactAssessment], context: Dict[str, Any]) -> List[str]:
        """Create an explainable reasoning chain for a projection.

        The chain references top contributing horizons and scenario assumptions.
        """
        chain: List[str] = []
        chain.append(f"Scenario: {scenario.name} - {scenario.description}")
        chain.append(f"Decision: {decision_summary}")

        # pick top 3 risk contributors from assessments
        contributors = []
        for a in assessments:
            try:
                contributors.append((getattr(a, "risk_score", 0.0), getattr(a, "horizon", getattr(a, "horizon", "unknown")), getattr(a, "description", "")))
            except Exception:
                continue
        contributors.sort(key=lambda x: x[0], reverse=True)
        top = contributors[:3]
        if top:
            chain.append("Top contributing horizons:")
            for score, horizon, desc in top:
                chain.append(f"- {horizon}: risk={round(float(score),4)}; note={desc}")
        else:
            chain.append("No detailed assessments available to identify contributors.")

        chain.append(f"Applied multiplier: {scenario.multiplier}")
        chain.append("Projection derived from deterministic aggregation of the consequence cascade to maintain explainability.")
        return chain

    def _synthesize_recommendations(self, base_actions: List[str], scenario: FutureScenario, assessments: List[ImpactAssessment], context: Dict[str, Any]) -> List[str]:
        """Produce actionable recommendations tuned to the scenario.

        Recommendations prefer stronger mitigations in pessimistic scenarios
        and monitoring/optimizations in optimistic ones.
        """
        actions: List[str] = []
        # Base recommended actions from cascade
        for a in base_actions:
            if a not in actions:
                actions.append(a)

        # Scenario specific augmentations
        if scenario.multiplier > 1.2:
            actions.insert(0, "Trigger full incident response playbook and executive alert.")
            actions.insert(1, "Activate contingency suppliers and prioritize critical orders.")
        elif scenario.multiplier < 0.8:
            actions.insert(0, "Defer escalation; prioritize monitoring and cost-optimized mitigations.")
        else:
            actions.insert(0, "Follow standard mitigation tasks and monitor KPIs.")

        # Limit verbosity: keep top 6 unique actions
        seen = set()
        trimmed: List[str] = []
        for a in actions:
            if a not in seen:
                trimmed.append(a)
                seen.add(a)
            if len(trimmed) >= 6:
                break
        return trimmed

    def _project_outcomes(self, decision_summary: str, scenario: FutureScenario, assessments: List[ImpactAssessment], context: Dict[str, Any], base_risk: float) -> Dict[str, Any]:
        """Create a compact projected_outcomes dictionary for downstream use.

        This includes aggregate risk metrics, likely SLA/customer outcomes,
        and estimated time-to-resolution heuristics when possible.
        """
        total_risk = 0.0
        impact_count = 0
        top_impacts: List[Dict[str, Any]] = []
        for a in assessments:
            try:
                rs = float(getattr(a, "risk_score", 0.0))
                total_risk += rs
                impact_count += 1
                top_impacts.append({
                    "horizon": getattr(a, "horizon", "unknown"),
                    "risk_score": round(rs * scenario.multiplier, 4),
                    "description": getattr(a, "description", ""),
                })
            except Exception:
                continue

        top_impacts.sort(key=lambda x: x.get("risk_score", 0.0), reverse=True)
        likely_customer_impact = any(("customer" in (x.get("horizon") or "").lower() and x.get("risk_score", 0.0) > 0.15) for x in top_impacts)

        avg_risk = (total_risk / impact_count) if impact_count else 0.0
        projected_total_risk = (base_risk + total_risk) * scenario.multiplier

        outcomes = {
            "projected_total_risk": round(projected_total_risk, 4),
            "projected_average_horizon_risk": round(avg_risk * scenario.multiplier, 4),
            "top_impacts": top_impacts[:5],
            "likely_customer_impact": bool(likely_customer_impact),
            "recommended_communication": ("Prepare customer communication and remediation offers." if likely_customer_impact else "Standard communications and monitoring."),
            "assumptions": [f"scenario_multiplier={scenario.multiplier}", f"shared_context_keys={list(self.shared_context.keys())}"],
        }
        return outcomes


__all__ = ["FutureTrajectoryEngine", "FutureProjection", "FutureScenario"]
