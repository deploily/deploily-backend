import logging
import os

import requests

_logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self):
        self.URL = os.getenv("PAYMENT_URL", "https://pay.demo.deploily.cloud/api/v1/epayment")
        self.STATUS_URL = os.getenv(
            "PAYMENT_STATUS_URL", "https://pay.demo.deploily.cloud/api/v1/epayment"
        )
        self.PDF_RECEIPT_URL = os.getenv("PDF_RECEIPT_URL", "")
        self.SEND_RECEIPT_MAIL_URL = os.getenv("SEND_RECEIPT_MAIL_URL", "")
        # TODO Get APIKey from ENV

    def post_payement(
        self, payment_id, total_amount, is_mvc_call, client_confirm_url, client_fail_url
    ):
        payload = {
            "ORDER_ID": payment_id,
            "NET_AMOUNT": int(total_amount),
            "IS_MVC_CALL": is_mvc_call,
            "CLIENT_CONFIRM_URL": client_confirm_url,
            "CLIENT_FAIL_URL": client_fail_url,
        }
        headers = {"Content-Type": "application/json"}

        _logger.info(f"[PAYMENT SERVICE] Sending payload: {payload}")

        try:
            response = requests.post(self.URL, json=payload, headers=headers)

            _logger.info(f"[PAYMENT SERVICE] Response status: {response.status_code}")
            _logger.info(f"[PAYMENT SERVICE] Response content: {response.text}")

            try:
                response_data = response.json()
            except requests.JSONDecodeError:
                _logger.error(f"Invalid JSON response from payment API: {response.text}")
                return {"message": "Invalid response from payment API"}, 500

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

    def get_payment_status(self, satim_order_id):
        params = {"SATIM_ORDER_ID": satim_order_id}
        try:
            response = requests.get(self.STATUS_URL, params=params)
            _logger.info(f"[PAYMENT SERVICE] Status check response content: {response.text}")
            _logger.info(f"[PAYMENT SERVICE] Status check response content: {type(response)}")
            return response
        except requests.RequestException as e:
            _logger.error(f"[PAYMENT SERVICE] Failed to check payment status: {str(e)}")
            return None

    def get_pdf_receipt(self, satim_order_id):
        params = {"SATIM_ORDER_ID": satim_order_id}
        try:
            response = requests.get(self.PDF_RECEIPT_URL, params=params)
            _logger.info(f"[PAYMENT SERVICE] Status check response content: {response.text}")
            _logger.info(f"[PAYMENT SERVICE] Status check response content: {type(response)}")
            return response
        except requests.RequestException as e:
            _logger.error(f"[PAYMENT SERVICE] Failed to check payment status: {str(e)}")
            return None

    def send_pdf_receipt_mail(self, satim_order_id, email):
        params = {"SATIM_ORDER_ID": satim_order_id, "EMAIL": email}
        try:
            response = requests.get(self.SEND_RECEIPT_MAIL_URL, params=params)
            _logger.info(f"[PAYMENT SERVICE] Status check response content: {response.text}")
            _logger.info(f"[PAYMENT SERVICE] Status check response content: {type(response)}")
            return response
        except requests.RequestException as e:
            _logger.error(f"[PAYMENT SERVICE] Failed to check payment status: {str(e)}")
            return None
