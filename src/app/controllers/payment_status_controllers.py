import logging

from flask import request
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required

from app import appbuilder
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
                    type: integer
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
            order_id = request.args.get("order_id", type=int)
            if not order_id:
                return self.response_400(
                    message="order_id est requis et doit être un entier valide."
                )

            payment_service = PaymentService()
            response = payment_service.get_payment_status(order_id)

            _logger.info(f"Statut de la réponse du service de paiement: {response.status_code}")
            _logger.info(f"Contenu brut de la réponse du service de paiement: {response.text}")

            if "application/json" in response.headers.get("Content-Type", ""):
                try:
                    response_data = response.json()
                except ValueError as e:
                    _logger.error(f"Erreur lors de l'analyse JSON de la réponse: {e}")
                    return self.response_500(
                        message="Erreur lors de l'analyse de la réponse du service de paiement."
                    )

                if (
                    response_data.get("ERRORCODE") == "0"
                    and response_data.get("ERRORMESSAGE") == "Success"
                ):
                    return self.response(200, status="success", details=response_data)
                else:
                    return self.response_400(
                        message="Échec de la vérification du paiement.",
                        error_code=response_data.get("ERRORCODE"),
                        details=response_data.get("ERRORMESSAGE"),
                    )
            else:
                _logger.error("Le service de paiement a renvoyé une réponse non-JSON.")
                return self.response_500(message="Réponse invalide du service de paiement.")

        except Exception as e:
            _logger.error(
                f"Erreur lors de la vérification du statut du paiement: {e}", exc_info=True
            )
            return self.response_500(message="Erreur interne du serveur.")


appbuilder.add_api(StatusApi)
