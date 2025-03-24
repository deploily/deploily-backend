import logging
import os

import requests

_logger = logging.getLogger(__name__)


class PaymentService:

    def __init__(self):
        self.URL = os.getenv("PAYMENT_URL", "http://192.168.1.14:5265/api/v1/epayment")

    def post_payement(self, payment_id, total_amount):
        payload = {"ORDER_ID": str(payment_id), "NET_AMOUNT": total_amount}

        headers = {"Content-Type": "application/json"}

        _logger.info(f"[PAYMENT SERVICE] Sending payload: {payload}")

        try:
            response = requests.post(self.URL, json=payload, headers=headers)

            _logger.info(f"[PAYMENT SERVICE] Response status: {response.status_code}")
            _logger.info(f"[PAYMENT SERVICE] Response content: {response.text}")

            if response.headers.get("Content-Type") == "application/json":
                try:
                    response_data = response.json() if response.text else {}
                except requests.JSONDecodeError:
                    _logger.error(f"Invalid JSON response from payment API: {response.text}")
                    return {"message": "Invalid response from payment API"}, 500
            else:
                _logger.error(f"Expected JSON response but got: {response.text}")
                return {"message": "Invalid response format from payment API"}, 500

            if (
                response.status_code != 200
                or not response_data.get("ORDER_ID")
                or not response_data.get("FORM_URL")
            ):
                _logger.error(f"Payment API Error: {response.status_code} - {response_data}")
                return {"message": "Payment Failed", "error": response_data}, 400

            return response_data, 200

        except requests.RequestException as e:
            _logger.error(f"[PAYMENT SERVICE] Failed to send payment data: {str(e)}")
            return {"message": "Payment processing error"}, 500
