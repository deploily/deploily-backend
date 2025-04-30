import logging

from flask import Response, request
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.models.payment_models import Payment
from app.models.subscription_models import Subscription
from app.services.payment_service import PaymentService

_logger = logging.getLogger(__name__)


class StatusApi(BaseApi):
    resource_name = "service-subscription"

    @expose("/payment-status", methods=["GET"])
    @protect()
    @jwt_required()
    def get_payment_status(self):
        """Checks the status of a payment using the order_id provided by the frontend.
        ---
        get:
            summary: Check the status of a payment
            description: Returns the payment status based on the provided order_id.
            parameters:
                - in: query
                  name: order_id
                  schema:
                    type: string
                  required: true
                  description: The order ID to check
            responses:
                200:
                    description: Payment status successfully retrieved
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    status:
                                        type: string
                                    details:
                                        type: object
                400:
                    description: Invalid request (missing or invalid parameters)
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
                                    message:
                                        type: string
                500:
                    description: Internal server error
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
        """

        try:
            order_id = request.args.get("order_id", type=str)
            if not order_id:
                return self.response_400(
                    message="order_id est requis et doit être un entier valide."
                )

            payment_service = PaymentService()
            response = payment_service.get_payment_status(order_id)
            try:
                response_data = response.json()
            except ValueError as e:
                _logger.error(f"Erreur lors de l'analyse JSON de la réponse: {e}")
                return self.response_500(
                    message="Erreur lors de l'analyse de la réponse du service de paiement."
                )

            if (
                response_data.get("ERROR_CODE") == "0"
                and response_data.get("ERROR_MESSAGE") == "Success"
            ):
                payment = db.session.query(Payment).filter_by(satim_order_id=order_id).first()
                if not payment:
                    return self.response_400(message="Payment not found")
                payment.status = "completed"
                subscription = (
                    db.session.query(Subscription).filter_by(id=payment.subscription_id).first()
                )
                if not subscription:
                    return self.response_400(message="subscription not found")
                subscription.payment_status = "paid"
                return self.response(200, status="success", details=response_data)
            else:
                return self.response(200, **response_data)

        except Exception as e:
            _logger.error(
                f"Erreur lors de la vérification du statut du paiement: {e}", exc_info=True
            )
            return self.response_500(message="Erreur interne du serveur.")

    @expose("/generate-pdf-receipt", methods=["GET"])
    @protect()
    @jwt_required()
    def get_pdf_receipt(self):
        """Generate payment receipt from payment module.
        ---
        get:
            summary: Check the status of a payment
            description: Returns the payment status based on the provided order_id.
            parameters:
                - in: query
                  name: order_id
                  schema:
                    type: string
                  required: true
                  description: The order ID to check
            responses:
                200:
                    description: Review Analysis
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    download_link:
                                        type: string
                                        format: uri
                                        example: /download
                400:
                    description: Invalid request (missing or invalid parameters)
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
                                    message:
                                        type: string
                500:
                    description: Internal server error
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
        """

        try:
            satim_order_id = request.args.get("order_id", type=str)
            if not satim_order_id:
                return self.response_400(
                    message="order_id est requis et doit être un entier valide."
                )

            payment_service = PaymentService()
            response = payment_service.get_pdf_receipt(satim_order_id)
            try:
                if response.status_code == 200:
                    # Extract filename from .NET response (if available)
                    filename = f"transaction_{satim_order_id}.pdf"
                    # Return the file with appropriate headers
                    return Response(
                        response.content,
                        mimetype="application/pdf",
                        headers={"Content-Disposition": f"attachment; filename={filename}"},
                    )
                return
            except ValueError as e:
                _logger.error(f"Erreur lors de l'analyse JSON de la réponse: {e}")
                return self.response_500(
                    message="Erreur lors de l'analyse de la réponse du service de paiement."
                )

        except Exception as e:
            _logger.error(
                f"Erreur lors de la vérification du statut du paiement: {e}", exc_info=True
            )
            return self.response_500(message="Erreur interne du serveur.")

    @expose("/send-pdf-receipt_mail", methods=["GET"])
    @protect()
    @jwt_required()
    def send_pdf_receipt_mail(self):
        """Send payment receipt from payment module.
        ---
        get:
            summary: Send the Payment receipt by mail.
            parameters:
                - in: query
                  name: order_id
                  schema:
                    type: string
                  required: true
                  description: The satim order ID
                - in: query
                  name: email
                  schema:
                    type: string
                  required: true
                  description: The email to send
            responses:
                200:
                    description: Review Analysis
                    content:
                        application/json:
                            schema:
                                type: string
                400:
                    description: Invalid request (missing or invalid parameters)
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
                                    message:
                                        type: string
                500:
                    description: Internal server error
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
        """

        try:
            satim_order_id = request.args.get("order_id", type=str)
            email = request.args.get("email", type=str)
            if not satim_order_id:
                return self.response_400(
                    message="order_id est requis et doit être un entier valide."
                )
            payment_service = PaymentService()
            response = payment_service.send_pdf_receipt_mail(satim_order_id, email)
            try:
                if response.status_code == 200:
                    return self.response(
                        200, status="success", details=response.content.decode("utf-8")
                    )
            except ValueError as e:
                _logger.error(f"Erreur lors de l'analyse JSON de la réponse: {e}")
                return self.response_500(
                    message="Erreur lors de l'analyse de la réponse du service de paiement."
                )

        except Exception as e:
            _logger.error(
                f"Erreur lors de la vérification du statut du paiement: {e}", exc_info=True
            )
            return self.response_500(message="Erreur interne du serveur.")


appbuilder.add_api(StatusApi)
