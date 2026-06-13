import os
import logging
from datetime import datetime
from typing import Any, Dict

import requests
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)


class VoiceAgent:
    def __init__(self):
        self.voice_endpoint = os.environ.get("VOICE_LIVE_ENDPOINT")
        self.voice_api_key = os.environ.get("VOICE_LIVE_API_KEY")
        self.order_status_url = os.environ.get("ORDER_LOGIC_APP_URL")
        self.event_grid_endpoint = os.environ.get("EVENT_GRID_TOPIC_ENDPOINT")
        self.event_grid_key = os.environ.get("EVENT_GRID_TOPIC_KEY")

        if not all(
            [
                self.voice_endpoint,
                self.voice_api_key,
                self.order_status_url,
                self.event_grid_endpoint,
                self.event_grid_key,
            ]
        ):
            raise ValueError(
                "Missing required environment variables. Please set "
                "VOICE_LIVE_ENDPOINT, VOICE_LIVE_API_KEY, ORDER_LOGIC_APP_URL, "
                "EVENT_GRID_TOPIC_ENDPOINT, and EVENT_GRID_TOPIC_KEY."
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.voice_api_key}",
                "Content-Type": "application/json",
            }
        )

    def _publish_event(self, event: Dict[str, Any]) -> None:
        headers = {
            "aeg-sas-key": self.event_grid_key,
            "Content-Type": "application/json",
        }

        response = requests.post(self.event_grid_endpoint, headers=headers, json=[event])
        response.raise_for_status()

        logger.info("Published Event Grid event: %s", event["eventType"])

    def _fetch_order_status(self, order_id: str) -> Dict[str, Any]:
        response = requests.get(f"{self.order_status_url.rstrip('/')}?orderId={order_id}")
        response.raise_for_status()

        logger.info("Retrieved order status for order %s", order_id)
        return response.json()

    def _answer_call(self, call_id: str) -> Dict[str, Any]:
        url = f"{self.voice_endpoint.rstrip('/')}/calls/{call_id}/answer"
        response = self.session.post(url, json={"action": "answer"})
        response.raise_for_status()

        logger.info("Answered inbound call %s", call_id)
        return response.json()

    def _play_text(self, call_id: str, text: str) -> Dict[str, Any]:
        url = f"{self.voice_endpoint.rstrip('/')}/calls/{call_id}/play"
        payload = {
            "voice": "alloy",
            "text": text,
        }

        response = self.session.post(url, json=payload)
        response.raise_for_status()

        logger.info("Played text to call %s", call_id)
        return response.json()

    def _hangup_call(self, call_id: str) -> None:
        url = f"{self.voice_endpoint.rstrip('/')}/calls/{call_id}"
        response = self.session.delete(url)
        response.raise_for_status()

        logger.info("Hung up call %s", call_id)

    def handle_inbound_call(self, data: Dict[str, Any]) -> Dict[str, Any]:
        call_id = data.get("callId") or data.get("call_id")
        customer_phone = data.get("from") or data.get("caller")
        order_id = data.get("orderId") or data.get("order_id")

        if not call_id or not customer_phone:
            logger.error("Inbound call event missing required fields: %s", data)
            raise ValueError("Inbound call data must include callId and from/caller")

        logger.info("Incoming call %s from %s", call_id, customer_phone)

        self._answer_call(call_id)

        order_data = None
        inquiry_status = "unknown"

        if order_id:
            try:
                order_data = self._fetch_order_status(order_id)
                inquiry_status = order_data.get("status", "unknown")

                message = (
                    f"Hello. We found order {order_id}. "
                    f"The current status is {inquiry_status}. "
                    "If you need additional help, please stay on the line."
                )

            except requests.HTTPError:
                logger.exception("Failed to retrieve order status for %s", order_id)

                message = (
                    "Hello. We could not look up your order at this time. "
                    "Please try again later or contact support."
                )
        else:
            message = (
                "Hello. We could not locate an order for your call. "
                "Please provide your order number to a customer service representative."
            )

        self._play_text(call_id, message)
        self._hangup_call(call_id)

        event = {
            "id": f"voice-signal-{call_id}-{int(datetime.utcnow().timestamp())}",
            "eventType": "signal.received",
            "subject": f"voice/order/{order_id or 'unknown'}/signal",
            "eventTime": datetime.utcnow().isoformat() + "Z",
            "data": {
                "signalSource": "Voice Agent",
                "signalType": "customer_inquiry",
                "callId": call_id,
                "customerPhone": customer_phone,
                "orderId": order_id,
                "orderStatus": inquiry_status,
                "payload": order_data,
            },
            "dataVersion": "1.0",
        }

        self._publish_event(event)

        return {
            "status": "processed",
            "eventType": "signal.received",
            "callId": call_id,
            "orderId": order_id,
        }


agent = VoiceAgent()


@app.route("/inbound-call", methods=["POST"])
def inbound_call_endpoint():
    payload = request.get_json(force=True)
    result = agent.handle_inbound_call(payload)
    return jsonify(result)


if __name__ == "__main__":
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 8080))

    logger.info("Starting VoiceAgent webhook server on %s:%s", host, port)
    app.run(host=host, port=port)