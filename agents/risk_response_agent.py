"""Risk Response Agent for NERVA multi-agent mesh.

Maps to Foundry agent ag-amosx-notify-prod with the role of Risk Response Agent.

Purpose:
Receives assessed risks from the Reasoning Agent and initiates mitigation,
escalation, approval, and notification workflows.

This module is dependency-free and contains no secrets or real connection strings.
"""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List

LOG = logging.getLogger("agents.risk_response_agent")


class RiskResponseAgent:
    """Agent that responds to assessed risks with mitigation and escalation.

    Attributes:
        agent_name: Mapped Foundry agent name.
        role: Architectural role name.
    """

    def __init__(self, agent_name: str = "ag-amosx-notify-prod", role: str = "Risk Response Agent") -> None:
        self.agent_name = agent_name
        self.role = role
        LOG.debug("Initialized RiskResponseAgent name=%s role=%s", self.agent_name, self.role)

    def respond_to_risk(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Produce a structured response for a given risk assessment.

        Args:
            risk_assessment: Mapping containing required risk fields.

        Returns:
            A dictionary with responseStatus, escalationLevel, mitigationAction,
            approvalRequired, targetStakeholders, notificationMessage,
            eventToPublish, and auditRecord.
        """
        required = (
            "riskId",
            "orderId",
            "eventType",
            "confidenceScore",
            "severity",
            "secondOrderConsequences",
            "thirdOrderFailures",
            "recommendedMitigation",
            "policyCitation",
        )

        missing = [k for k in required if k not in risk_assessment]
        if missing:
            LOG.warning("Risk assessment missing keys: %s", missing)

        # Normalize inputs
        confidence = float(risk_assessment.get("confidenceScore", 0.0))
        severity_raw = str(risk_assessment.get("severity", "unknown"))
        severity = severity_raw.strip().lower()

        # Escalation logic
        if confidence >= 0.90 or severity == "critical":
            escalation = "P1"
        elif confidence >= 0.75:
            escalation = "P2"
        else:
            escalation = "P3"

        # Mitigation action: prefer recommendedMitigation from assessment
        mitigation_action = risk_assessment.get("recommendedMitigation") or "Investigate and monitor"

        # Approval required for highest-severity or P1
        approval_required = escalation == "P1" or severity == "critical"

        # Select stakeholders based on escalation
        if escalation == "P1":
            stakeholders: List[str] = ["Risk Board", "Executive Ops", "Legal", "Customer Success"]
        elif escalation == "P2":
            stakeholders = ["Ops Team", "Product Manager", "Risk Owner"]
        else:
            stakeholders = ["Assigned Owner"]

        risk_id = risk_assessment.get("riskId")
        order_id = risk_assessment.get("orderId")

        notification_message = (
            f"Risk {risk_id} for order {order_id}: severity={risk_assessment.get('severity')} "
            f"confidence={confidence:.2f} escalation={escalation}."
            f" Recommended action: {mitigation_action}"
        )

        event_to_publish = {
            "eventType": "RiskResponseInitiated",
            "riskId": risk_id,
            "orderId": order_id,
            "escalationLevel": escalation,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        audit_record = {
            "auditId": str(uuid.uuid4()),
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "agent": self.agent_name,
            "inputSnapshot": risk_assessment,
            "decision": {
                "escalation": escalation,
                "mitigation": mitigation_action,
                "approvalRequired": approval_required,
                "notified": stakeholders,
            },
        }

        # Derive high-level response status
        if escalation in ("P1", "P2"):
            response_status = "escalated"
        else:
            response_status = "monitoring"

        response = {
            "responseStatus": response_status,
            "escalationLevel": escalation,
            "mitigationAction": mitigation_action,
            "approvalRequired": approval_required,
            "targetStakeholders": stakeholders,
            "notificationMessage": notification_message,
            "eventToPublish": event_to_publish,
            "auditRecord": audit_record,
        }

        LOG.info("Responded to risk %s with escalation=%s approval=%s", risk_id, escalation, approval_required)
        LOG.debug("Response payload: %s", json.dumps(response, default=str))

        return response


def _sample_risk_assessment() -> Dict[str, Any]:
    return {
        "riskId": "RISK-ORD-1009-01",
        "orderId": "ORD-1009",
        "eventType": "RevenueExposure",
        "confidenceScore": 0.92,
        "severity": "High",
        "secondOrderConsequences": "Revenue at risk; potential SLA breach",
        "thirdOrderFailures": "Customer churn; financial penalty",
        "recommendedMitigation": "Pause fulfillment; Open incident; Escalate to finance for hold approval",
        "policyCitation": "sla-policy-enterprise#section-4.2",
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    LOG.setLevel(logging.DEBUG)

    agent = RiskResponseAgent()
    assessment = _sample_risk_assessment()
    response = agent.respond_to_risk(assessment)

    print("Risk Response for ORD-1009:\n")
    print(json.dumps(response, indent=2, default=str))
