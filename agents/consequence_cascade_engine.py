"""Consequence Cascade Reasoning Engine for NERVA

This module implements the Consequence Cascade methodology used by the
NERVA Autonomous Enterprise Nervous System. It evaluates a proposed
decision and predicts consequences across multiple horizons, computes
confidence and risk scores, produces reasoning chains, and returns
JSON-serializable results suitable for logging or downstream simulation.

The implementation is designed to be imported and called by
`agents/reasoning_agent.py` and to integrate with `AgentLog`, shared
enterprise context, and future NERVA Resonance simulators.

Example usage:

    from agents.consequence_cascade import ConsequenceCascadeEngine

    engine = ConsequenceCascadeEngine(agent_log=agent_log, shared_context=sec)
    result = engine.assess_decision(
        decision_id="DEC-123",
        decision_summary="Delay shipment of SKU-42 by 48 hours due to quality check",
        context={"order_id": "ORD-555"}
    )
    # `result` is dataclass-style and JSON-serializable via `result.to_dict()`

"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import math
import logging

logger = logging.getLogger(__name__)


HORIZONS = [
    "Immediate Effects",
    "Operational impact",
    "SLA impact",
    "Resource impact",
    "Downstream Effects",
    "Cross-functional dependencies",
    "Inventory implications",
    "Carrier and supplier implications",
    "Customer experience impact",
    "Long-Term Effects",
    "Strategic impact",
    "Financial impact",
    "Organizational learning impact",
    "Risk accumulation",
]


@dataclass
class ImpactAssessment:
    """Assessment for a single consequence horizon.

    Attributes:
        horizon: Name of the consequence horizon (e.g., "Immediate Effects").
        description: Short natural-language summary of the predicted consequence.
        severity: Estimated severity on [0.0, 1.0].
        likelihood: Estimated likelihood on [0.0, 1.0].
        confidence: Confidence in this assessment on [0.0, 1.0].
        risk_score: Derived risk score (severity * likelihood).
        reasoning_chain: Stepwise explanations used to reach the assessment.
        recommended_actions: Concrete recommended mitigations or next steps.
    """

    horizon: str
    description: str
    severity: float
    likelihood: float
    confidence: float
    risk_score: float = field(init=False)
    reasoning_chain: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Ensure numeric ranges and compute derived risk_score
        self.severity = max(0.0, min(1.0, float(self.severity)))
        self.likelihood = max(0.0, min(1.0, float(self.likelihood)))
        self.confidence = max(0.0, min(1.0, float(self.confidence)))
        self.risk_score = round(self.severity * self.likelihood, 4)


@dataclass
class ConsequenceResult:
    """Top-level result produced by the ConsequenceCascadeEngine.

    Attributes:
        decision_id: External identifier for the assessed decision.
        decision_summary: Short text describing the decision under evaluation.
        timestamp: ISO-8601 UTC timestamp when the assessment completed.
        overall_confidence: Aggregated confidence across horizons.
        overall_risk_score: Aggregated risk across horizons.
        assessments: List of `ImpactAssessment` objects for each horizon.
        recommended_actions: Aggregated recommended actions.
        metadata: Optional dictionary with extra diagnostics for agents.
    """

    decision_id: Optional[str]
    decision_summary: str
    timestamp: str
    overall_confidence: float
    overall_risk_score: float
    assessments: List[ImpactAssessment]
    recommended_actions: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation of the result."""
        d = asdict(self)
        # Ensure nested dataclasses are converted properly (they already are via asdict)
        return d


class ConsequenceCascadeEngine:
    """Engine that evaluates decisions and produces consequence cascade results.

    The engine uses lightweight heuristics to produce severity/likelihood
    estimates, confidence and risk scores, reasoning chains, and recommended
    actions. It is intentionally designed as a reusable component that can
    be integrated into agent pipelines, logging systems, and simulation
    platforms.

    Integration hooks:
        - `agent_log`: optional object exposing `log(event_type, payload)`.
        - `shared_context`: optional dictionary-like shared enterprise context.
        - `resonance_adapter`: optional adapter for future simulation ingestion.
    """

    def __init__(
        self,
        agent_log: Optional[Any] = None,
        shared_context: Optional[Dict[str, Any]] = None,
        resonance_adapter: Optional[Any] = None,
    ) -> None:
        self.agent_log = agent_log
        self.shared_context = shared_context or {}
        self.resonance_adapter = resonance_adapter

    def assess_decision(self, decision_summary: str, decision_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> ConsequenceResult:
        """Assess a decision and return a `ConsequenceResult`.

        Args:
            decision_summary: Text description of the proposed decision.
            decision_id: Optional external identifier for traceability.
            context: Optional additional context dictionary (e.g., order info).

        Returns:
            A `ConsequenceResult` instance with per-horizon assessments.
        """
        context = context or {}
        timestamp = datetime.utcnow().isoformat() + "Z"

        assessments: List[ImpactAssessment] = []
        for horizon in HORIZONS:
            severity, likelihood = self._estimate_severity_likelihood(decision_summary, horizon, context)
            confidence = self._estimate_confidence(decision_summary, horizon, context, severity, likelihood)
            reasoning = self._generate_reasoning_chain(decision_summary, horizon, severity, likelihood, context)
            actions = self._recommend_actions(horizon, severity, likelihood, confidence, context)

            assessment = ImpactAssessment(
                horizon=horizon,
                description=reasoning[0] if reasoning else f"Predicted consequence for {horizon}",
                severity=severity,
                likelihood=likelihood,
                confidence=confidence,
                reasoning_chain=reasoning,
                recommended_actions=actions,
            )
            assessments.append(assessment)

        overall_confidence = self._aggregate_confidence(assessments)
        overall_risk_score = self._aggregate_risk(assessments)

        aggregated_actions = self._aggregate_actions(assessments)

        result = ConsequenceResult(
            decision_id=decision_id,
            decision_summary=decision_summary,
            timestamp=timestamp,
            overall_confidence=round(overall_confidence, 4),
            overall_risk_score=round(overall_risk_score, 4),
            assessments=assessments,
            recommended_actions=aggregated_actions,
            metadata={
                "source": "consequence_cascade",
                "shared_context_keys": list(self.shared_context.keys()),
            },
        )

        # Attempt to log to AgentLog if provided
        try:
            if self.agent_log and hasattr(self.agent_log, "log"):
                self.agent_log.log("consequence_assessment", result.to_dict())
        except Exception:
            logger.exception("Failed to write to agent_log")

        # Optionally send to resonance adapter for future simulation
        try:
            if self.resonance_adapter and hasattr(self.resonance_adapter, "ingest"):
                self.resonance_adapter.ingest(result.to_dict())
        except Exception:
            logger.exception("Failed to send to resonance_adapter")

        return result

    # -- Core heuristic helpers -------------------------------------------------
    def _estimate_severity_likelihood(self, text: str, horizon: str, context: Dict[str, Any]) -> (float, float):
        """Estimate severity and likelihood for a given horizon.

        This method uses deterministic heuristics so results are explainable
        and unit-testable. Implementations can be replaced by ML models
        without changing the public API.
        """
        t = text.lower()
        base_severity = 0.1
        base_likelihood = 0.1

        keywords_severity = {
            "delay": 0.2,
            "disrupt": 0.3,
            "outage": 0.5,
            "failure": 0.5,
            "cancel": 0.4,
            "quality": 0.25,
            "recall": 0.6,
            "cost": 0.2,
            "accelerate": -0.05,
            "expedite": -0.05,
        }

        multiplier = 1.0
        # horizon-sensitive adjustments
        if "sla" in horizon.lower():
            multiplier += 0.15
        if "inventory" in horizon.lower() or "carrier" in horizon.lower():
            multiplier += 0.1
        if "financial" in horizon.lower() or "strategic" in horizon.lower():
            multiplier += 0.2

        sev = base_severity
        lik = base_likelihood
        for k, v in keywords_severity.items():
            if k in t:
                sev += max(0.0, v) * multiplier
                lik += abs(v) * 0.8 * multiplier

        # Use context signals (e.g., high-value order) to increase severity/likelihood
        if context.get("priority") in ("high", "urgent"):
            sev += 0.15
            lik += 0.1
        if context.get("order_value") and float(context.get("order_value", 0)) > 100000:
            sev += 0.2
            lik += 0.15

        # Horizon-specific bounds and adjustments
        if "customer" in horizon.lower():
            # Customer impact often has higher likelihood when decisions affect SLA or inventory
            lik = min(1.0, lik + 0.05)

        # Normalize
        sev = min(1.0, sev)
        lik = min(1.0, lik)
        return round(sev, 4), round(lik, 4)

    def _estimate_confidence(self, text: str, horizon: str, context: Dict[str, Any], severity: float, likelihood: float) -> float:
        """Estimate confidence in the assessment.

        Confidence decreases when severity or likelihood are uncertain (near 0.5)
        and increases with context signals or short, precise decisions.
        """
        confidence = 0.6
        # length heuristic: very short text -> lower confidence
        if len(text.split()) < 4:
            confidence -= 0.15
        if len(text.split()) > 15:
            confidence += 0.05

        # if context contains strong signals, raise confidence
        if context:
            confidence += 0.1

        # uncertainty penalty: if severity and likelihood diverge, reduce confidence
        confidence -= abs(severity - likelihood) * 0.2

        # clamp
        confidence = max(0.05, min(0.99, confidence))
        return round(confidence, 4)

    def _generate_reasoning_chain(self, text: str, horizon: str, severity: float, likelihood: float, context: Dict[str, Any]) -> List[str]:
        """Create a short stepwise reasoning chain for explainability."""
        steps: List[str] = []
        steps.append(f"Horizon matched: {horizon}.")
        if severity > 0.6:
            steps.append("Estimated severity is high based on keywords and context.")
        elif severity > 0.3:
            steps.append("Estimated severity is moderate.")
        else:
            steps.append("Estimated severity is low.")

        if likelihood > 0.6:
            steps.append("Likely to occur given historical patterns and context.")
        elif likelihood > 0.3:
            steps.append("Possible occurrence under certain conditions.")
        else:
            steps.append("Unlikely but possible; monitor relevant signals.")

        # Add context-based steps
        if context.get("order_id"):
            steps.append(f"Context includes order_id={context.get('order_id')}; tie to downstream order processing.")
        if context.get("priority"):
            steps.append(f"Priority flagged as {context.get('priority')} increasing impact attention.")

        steps.append(f"Derived risk_score={round(severity * likelihood, 4)} and confidence={round(self._estimate_confidence(text, horizon, context, severity, likelihood), 4)}.")
        return steps

    def _recommend_actions(self, horizon: str, severity: float, likelihood: float, confidence: float, context: Dict[str, Any]) -> List[str]:
        """Return a short list of recommended actions for mitigation or monitoring."""
        actions: List[str] = []
        # Thresholds for recommended actions
        risk = severity * likelihood
        if risk >= 0.5:
            actions.append("Escalate to incident response and notify stakeholders.")
            actions.append("Execute contingency plan: engage alternative suppliers/carriers.")
        elif risk >= 0.2:
            actions.append("Open a mitigation task and monitor key metrics closely.")
            actions.append("Notify operations for potential manual intervention.")
        else:
            actions.append("Monitor; no immediate action required unless metrics change.")

        # Add horizon-specific suggestions
        if "sla" in horizon.lower():
            actions.append("Review SLA thresholds and contact account management if at risk.")
        if "inventory" in horizon.lower():
            actions.append("Check safety stock levels and trigger reorder if below threshold.")
        if "carrier" in horizon.lower() or "supplier" in horizon.lower():
            actions.append("Validate carrier ETAs and confirm supplier lead times.")
        if "customer" in horizon.lower():
            actions.append("Prepare customer communication templates and offer alternatives.")

        # De-duplicate and trim actions
        unique_actions = []
        for a in actions:
            if a not in unique_actions:
                unique_actions.append(a)
        return unique_actions

    # -- Aggregation helpers ---------------------------------------------------
    def _aggregate_confidence(self, assessments: List[ImpactAssessment]) -> float:
        if not assessments:
            return 0.0
        # Weighted average: weight by risk magnitude (severity * likelihood)
        total_weight = 0.0
        weighted_conf = 0.0
        for a in assessments:
            w = a.severity * a.likelihood + 0.0001
            total_weight += w
            weighted_conf += a.confidence * w
        return weighted_conf / total_weight if total_weight > 0 else 0.0

    def _aggregate_risk(self, assessments: List[ImpactAssessment]) -> float:
        # Aggregate risk as the max of per-horizon risk scores, but also include
        # a small contribution of the sum to reflect multi-horizon accumulation.
        if not assessments:
            return 0.0
        max_risk = max(a.risk_score for a in assessments)
        sum_risk = sum(a.risk_score for a in assessments)
        # Combine with diminishing returns on the sum
        combined = max_risk + math.log1p(sum_risk) * 0.1
        return combined

    def _aggregate_actions(self, assessments: List[ImpactAssessment]) -> List[str]:
        actions = []
        for a in assessments:
            for act in a.recommended_actions:
                if act not in actions:
                    actions.append(act)
        return actions


__all__ = ["ConsequenceCascadeEngine", "ConsequenceResult", "ImpactAssessment"]
