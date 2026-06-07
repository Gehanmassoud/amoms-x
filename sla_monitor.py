import os
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class SLAMonitor:
    def __init__(self):
        self.logic_app_url = os.environ.get("SLA_LOGIC_APP_URL")
        self.search_endpoint = os.environ.get("SLA_SEARCH_ENDPOINT")
        self.search_api_key = os.environ.get("SLA_SEARCH_API_KEY")
        self.event_grid_endpoint = os.environ.get("EVENT_GRID_TOPIC_ENDPOINT")
        self.event_grid_key = os.environ.get("EVENT_GRID_TOPIC_KEY")

        if not all([self.logic_app_url, self.search_endpoint, self.search_api_key, self.event_grid_endpoint, self.event_grid_key]):
            raise ValueError(
                "Missing required environment variables. Please set SLA_LOGIC_APP_URL, SLA_SEARCH_ENDPOINT, SLA_SEARCH_API_KEY, EVENT_GRID_TOPIC_ENDPOINT, and EVENT_GRID_TOPIC_KEY."
            )

    def _fetch_order_record(self, order_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.logic_app_url.rstrip('/')}?orderId={order_id}")
        response.raise_for_status()
        logger.info("Fetched order record for order %s", order_id)
        return response.json()

    def _fetch_sla_policies(self, search_query: str) -> List[Dict[str, Any]]:
        headers = {
            "Content-Type": "application/json",
            "api-key": self.search_api_key,
        }
        payload = {
            "query": search_query,
            "top": 5,
            "answers": "none",
        }
        response = requests.post(self.search_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        policies = result.get("value") or result.get("results") or []
        logger.info("Retrieved %d SLA policy documents for query '%s'", len(policies), search_query)
        return policies

    def _derive_policy_thresholds(self, policies: List[Dict[str, Any]]) -> Dict[str, Any]:
        thresholds = {
            "responseHours": 24,
            "resolutionHours": 72,
            "deliveryHours": 96,
        }
        for policy in policies:
            content = json.dumps(policy).lower()
            if "response" in content and "4 hours" in content:
                thresholds["responseHours"] = min(thresholds["responseHours"], 4)
            if "resolution" in content and "24 hours" in content:
                thresholds["resolutionHours"] = min(thresholds["resolutionHours"], 24)
            if "delivery" in content and "48 hours" in content:
                thresholds["deliveryHours"] = min(thresholds["deliveryHours"], 48)
        logger.info("Derived SLA thresholds: %s", thresholds)
        return thresholds

    def _evaluate_sla(self, order: Dict[str, Any], thresholds: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow()
        order_created = self._parse_datetime(order.get("createdAt")) or now
        promised = self._parse_datetime(order.get("promisedAt"))
        last_update = self._parse_datetime(order.get("lastUpdate")) or order_created

        response_deadline = order_created + timedelta(hours=thresholds["responseHours"])
        resolution_deadline = order_created + timedelta(hours=thresholds["resolutionHours"])
        delivery_deadline = promised if promised else order_created + timedelta(hours=thresholds["deliveryHours"])

        breach_reasons = []
        if now > response_deadline and order.get("status") in {"new", "pending", "review"}:
            breach_reasons.append("Missed initial response SLA")
        if now > resolution_deadline and order.get("status") in {"pending", "issue", "escalated"}:
            breach_reasons.append("Missed resolution SLA")
        if promised and now > delivery_deadline and order.get("status") != "complete":
            breach_reasons.append("Missed promised delivery SLA")

        risk_reasons = []
        if now + timedelta(hours=4) > response_deadline and now <= response_deadline:
            risk_reasons.append("At risk of missing response SLA")
        if now + timedelta(hours=8) > resolution_deadline and now <= resolution_deadline:
            risk_reasons.append("At risk of missing resolution SLA")

        result = {
            "orderId": order.get("orderId"),
            "status": order.get("status"),
            "responseDeadline": response_deadline.isoformat() + "Z",
            "resolutionDeadline": resolution_deadline.isoformat() + "Z",
            "deliveryDeadline": delivery_deadline.isoformat() + "Z",
            "breach": len(breach_reasons) > 0,
            "breachReasons": breach_reasons,
            "riskReasons": risk_reasons,
            "orderData": order,
        }
        logger.info("SLA evaluation result: breach=%s", result["breach"])
        return result

    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"]:
            try:
                return datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                continue
        logger.warning("Unable to parse datetime value: %s", value)
        return None

    def _publish_breach_event(self, evaluation: Dict[str, Any]) -> None:
        event = {
            "id": f"sla-breach-{evaluation['orderId']}-{int(datetime.utcnow().timestamp())}",
            "eventType": "sla.breach",
            "subject": f"order/{evaluation['orderId']}/sla",
            "eventTime": datetime.utcnow().isoformat() + "Z",
            "data": {
                "orderId": evaluation["orderId"],
                "status": evaluation["status"],
                "breach": evaluation["breach"],
                "breachReasons": evaluation["breachReasons"],
                "riskReasons": evaluation["riskReasons"],
                "responseDeadline": evaluation["responseDeadline"],
                "resolutionDeadline": evaluation["resolutionDeadline"],
                "deliveryDeadline": evaluation["deliveryDeadline"],
            },
            "dataVersion": "1.0",
        }
        headers = {
            "aeg-sas-key": self.event_grid_key,
            "Content-Type": "application/json",
        }
        response = requests.post(self.event_grid_endpoint, headers=headers, json=[event])
        response.raise_for_status()
        logger.info("Published sla.breach event for order %s", evaluation["orderId"])

    def assess_order_sla(self, order_id: str) -> Dict[str, Any]:
        # Step 1: Retrieve order record from Azure SQL via Logic App.
        order = self._fetch_order_record(order_id)

        # Step 2: Retrieve SLA policies from Azure AI Search Foundry IQ.
        search_terms = order.get("serviceType") or order.get("productType") or order.get("orderType") or "SLA"
        sla_policies = self._fetch_sla_policies(search_terms)

        # Step 3: Derive applicable thresholds from policy content.
        thresholds = self._derive_policy_thresholds(sla_policies)

        # Step 4: Evaluate the order against SLA thresholds.
        evaluation = self._evaluate_sla(order, thresholds)

        # Step 5: Publish an SLA breach event if a breach is present.
        if evaluation["breach"]:
            self._publish_breach_event(evaluation)

        return evaluation


def main():
    import argparse

    parser = argparse.ArgumentParser(description="AMOMS-X SLA Monitor")
    parser.add_argument("orderId", help="Order ID to evaluate against SLA policies")
    args = parser.parse_args()

    monitor = SLAMonitor()
    result = monitor.assess_order_sla(args.orderId)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
