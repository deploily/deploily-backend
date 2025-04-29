import json
import logging

from flask import request
from flask_appbuilder.api import BaseApi, expose, protect, rison
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.models import Payment, PaymentProfile
from app.services.payment_service import PaymentService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class AccountFundingApi(BaseApi):
    resource_name = "balance"

    @expose("/fund-balance", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def fund_balance(self, **kwargs):
        """
        Fund balance.
        ---
        post:
            summary: Fund balance
            description: Fund balance.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                profile_id:
                                    type: integer
                                    description: ID of the user's profile
                                total_amount:
                                    type: number
                                    format: float
                                    description: Total amount before applying promo codes
                                payment_method:
                                    type: string
                                    description: Payment method (e.g., "card", "paypal")
            responses:
                200:
                    description: Payment successful
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    order_id:
                                        type: string
                                    form_url:
                                        type: string
                                    new_balance:
                                        type: number
                400:
                    description: Bad request
                500:
                    description: Internal server error
        """
        try:
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            data = request.get_json(silent=True)
            if not data:
                return self.response_400(message="Invalid request data")

            profile_id = data.get("profile_id")
            total_amount = data.get("total_amount")
            payment_method = data.get("payment_method", "card")

            if not profile_id:
                return self.response_400(message="Profile ID is required")
            if not total_amount:
                return self.response_400(message="Total amount is required")
            if not payment_method:
                return self.response_400(message="Payment method is required")

            profile = (
                db.session.query(PaymentProfile).filter_by(created_by=user, id=profile_id).first()
            )
            if not profile:
                return self.response_400(message="Profile not found")

            payment = Payment(
                amount=total_amount,
                payment_method=payment_method,
                profile_id=profile.id,
                status="pending",
            )
            db.session.add(payment)
            db.session.commit()

            satim_order_id = ""
            form_url = ""

            if payment_method == "card" and profile.profile_type != "default":
                payment.order_id = f"PAY{payment.id}"
                db.session.commit()

                payment_service = PaymentService()
                try:
                    response = payment_service.post_payement(payment.order_id, total_amount)[0]
                    if isinstance(response, str):
                        response = json.loads(response)
                except Exception:
                    _logger.error("Error calling payment service", exc_info=True)
                    return self.response_500(message="Payment service error")

                if not isinstance(response, dict):
                    return self.response_500(message="Invalid payment service response")

                if response.get("ERROR_CODE") != "0":
                    return self.response_400(
                        message="Payment failed",
                        details=response.get("ERROR_MESSAGE", "Unknown error"),
                    )

                satim_order_id = response.get("ORDER_ID")
                form_url = response.get("FORM_URL")
                payment.satim_order_id = satim_order_id

                db.session.commit()

            profile.balance

            return self.response(
                200,
                **{
                    "order_id": satim_order_id,
                    "form_url": form_url,
                },
            )

        except Exception as e:
            _logger.error(f"Error in fund_balance: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")


appbuilder.add_api(AccountFundingApi)
