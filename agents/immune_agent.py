import os
import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List

import requests

from nerva_modes import NervaMode

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class ImmuneAgent:
    def __init__(self):
        self.logic_app_url = os.environ.get("IMMUNE_LOGIC_APP_URL")
        self.search_endpoint = os.environ.get("IMMUNE_SEARCH_ENDPOINT")
        self.search_api_key = os.environ.get("IMMUNE_SEARCH_API_KEY")
        self.event_grid_endpoint = os.environ.get("EVENT_GRID_TOPIC_ENDPOINT")
        self.event_grid_key = os.environ.get("EVENT_GRID_TOPIC_KEY")
        self.poll_interval_minutes = int(os.environ.get("IMMUNE_POLL_INTERVAL_MINUTES", "15"))

        if not all([self.logic_app_url, self.search_endpoint, self.search_api_key, self.event_grid_endpoint, self.event_grid_key]):
            raise ValueError(
                "Missing required environment variables. Please set IMMUNE_LOGIC_APP_URL, IMMUNE_SEARCH_ENDPOINT, IMMUNE_SEARCH_API_KEY, EVENT_GRID_TOPIC_ENDPOINT, and EVENT_GRID_TOPIC_KEY."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "api-key": self.search_api_key,
        })

    def _fetch_carrier_performance(self) -> List[Dict[str, Any]]:
        response = requests.get(self.logic_app_url)
        response.raise_for_status()
        data = response.json()
        logger.info("Fetched carrier performance data with %d records", len(data) if isinstance(data, list) else 1)
        return data if isinstance(data, list) else [data]

    def _detect_anomalies(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        anomalies: List[Dict[str, Any]] = []
        for record in records:
            carrier = record.get("carrierId") or record.get("carrier") or "unknown"
            metrics = record.get("metrics", {})
            latency = float(metrics.get("latencyMs", 0))
            failure_rate = float(metrics.get("failureRate", 0))
            pickup_delay = float(metrics.get("pickupDelayMinutes", 0))
            on_time_percentage = float(metrics.get("onTimePercentage", 100))

            confidence = 0.0
            reasons = []

            if latency > 2000:
                confidence += 0.35
                reasons.append("High latency")
            elif latency > 1200:
                confidence += 0.15
                reasons.append("Elevated latency")

            if failure_rate > 0.10:
                confidence += 0.35
                reasons.append("Elevated failure rate")
            elif failure_rate > 0.05:
                confidence += 0.15
                reasons.append("Increased failure rate")

            if pickup_delay > 60:
                confidence += 0.20
                reasons.append("Long pickup delay")
            elif pickup_delay > 30:
                confidence += 0.10
                reasons.append("Moderate pickup delay")

            if on_time_percentage < 85:
                confidence += 0.25
                reasons.append("Low on-time performance")
            elif on_time_percentage < 92:
                confidence += 0.10
                reasons.append("Below-target on-time performance")

            confidence = min(confidence, 1.0)
            if confidence > 0:
                anomalies.append({
                    "carrierId": carrier,
                    "metrics": metrics,
                    "confidence": round(confidence, 2),
                    "reasons": reasons,
                    "record": record,
                })
        anomalies.sort(key=lambda item: item["confidence"], reverse=True)
        logger.info("Detected %d anomalies", len(anomalies))
        return anomalies

    def _query_escalation_procedures(self, carrier_id: str, anomaly_reasons: List[str]) -> List[Dict[str, Any]]:
        query = f"carrier escalation procedures {carrier_id} {' '.join(anomaly_reasons)}"
        payload = {
            "query": query,
            "top": 3,
            "answers": "none",
        }
        response = self.session.post(self.search_endpoint, json=payload)
        response.raise_for_status()
        result = response.json()
        items = result.get("value") or result.get("results") or []
        logger.info("Found %d escalation procedure documents for carrier %s", len(items), carrier_id)
        return items

    def _publish_risk_event(self, anomaly: Dict[str, Any], procedures: List[Dict[str, Any]]) -> None:
        event = {
            "id": f"risk-emerging-{anomaly['carrierId']}-{int(datetime.utcnow().timestamp())}",
            "eventType": "nerva.immune.threat_detected",
            "subject": f"nerva/immune/carrier/{anomaly['carrierId']}",
            "eventTime": datetime.utcnow().isoformat() + "Z",
            "data": {
                "nervaMode": NervaMode.IMMUNE,
                "signalSource": "Immune Agent",
                "signalType": "carrier_anomaly",

                "contextRequired": True,
                "reasoningRequired": True,
                "cascadeAnalysisRequired": True,
                "futureTrajectoryRequired": True,
                "riskAssessmentRequired": True,

                "carrierId": anomaly["carrierId"],
                "confidence": anomaly["confidence"],
                "reasons": anomaly["reasons"],
                "metrics": anomaly["metrics"],
                "escalationProcedures": procedures,
            },
            "dataVersion": "1.0",
        }
        headers = {
            "aeg-sas-key": self.event_grid_key,
            "Content-Type": "application/json",
        }
        response = requests.post(self.event_grid_endpoint, headers=headers, json=[event])
        response.raise_for_status()
        logger.info("Published nerva.immune.threat_detected event for carrier %s with confidence %s", anomaly["carrierId"], anomaly["confidence"])

    def run_scan(self) -> None:
        records = self._fetch_carrier_performance()
        anomalies = self._detect_anomalies(records)
        for anomaly in anomalies:
            procedures = []

            if anomaly["confidence"] >= 0.7:
                procedures = self._query_escalation_procedures(
                    anomaly["carrierId"],
                    anomaly["reasons"]
                )

            self._publish_risk_event(anomaly, procedures)

    def start(self) -> None:
        interval_seconds = self.poll_interval_minutes * 60
        logger.info("Starting Immune Agent with %d-minute scan interval", self.poll_interval_minutes)
        while True:
            try:
                self.run_scan()
            except Exception as exc:
                logger.exception("Immune Agent scan failed: %s", exc)
            time.sleep(interval_seconds)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="AMOMS-X Immune Agent")
    parser.add_argument("--once", action="store_true", help="Run a single scan and exit")
    args = parser.parse_args()

    agent = ImmuneAgent()
    if args.once:
        agent.run_scan()
    else:
        agent.start()


if __name__ == "__main__":
    main()
