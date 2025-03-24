import logging
from datetime import datetime

from flask import request
from flask_appbuilder.api import BaseApi, expose, protect, rison
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.models import Payment, Profile, PromoCode, ServicePlan, Subscribe
from app.services.payment_service import PaymentService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class SubscriptionApi(BaseApi):
    resource_name = "service-subscription"

    @expose("/subscribe", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def subscribe_to_plan(self, **kwargs):
        """Subscribe a user to a service plan.
        ---
        post:
            summary: Subscribe a user to a service plan
            description: Creates a new subscription for the authenticated user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                service_plan_selected_id:
                                    type: integer
                                    description: ID of the selected service plan
                                total_amount:
                                    type: number
                                    format: float
                                    description: Total amount before applying promo codes
                                promo_code_profile_selected_id:
                                    type: string
                                    description: Promo code (if applicable)
                                duration:
                                    type: integer
                                    description: Duration of the subscription in months
                                payment_method:
                                    type: string
                                    description: Payment method (e.g., "card", "paypal")
            responses:
                200:
                    description: Subscription successful
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    subscription:
                                        type: object
                                        properties:
                                            id:
                                                type: integer
                                            name:
                                                type: string
                                            start_date:
                                                type: string
                                                format: date-time
                                            total_amount:
                                                type: number
                                            price:
                                                type: number
                                            status:
                                                type: string
                                            duration_month:
                                                type: integer
                                            service_plan_id:
                                                type: integer
                                            promo_code_id:
                                                type: integer
                                                nullable: true
                                    order_id:
                                        type: string
                                    form_url:
                                        type: string
                400:
                    description: Bad request (invalid input)
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
                                    message:
                                        type: string
                404:
                    description: Resource not found (e.g., user, plan, or profile)
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
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
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            profile = db.session.query(Profile).filter_by(user_id=user.id).first()
            if not profile:
                return self.response_400(message="Profile not found")

            if profile.balance is None:
                return self.response_404(message="Insufficient balance")

            data = request.get_json(silent=True)
            if not data:
                return self.response_400(message="Invalid request data")

            plan_id = data.get("service_plan_selected_id")
            plan = db.session.query(ServicePlan).filter_by(id=plan_id).first()
            if not plan:
                return self.response_400(message="Service Plan not found")

            total_amount = data.get("total_amount")
            promo_code_str = data.get("promo_code_profile_selected_id")
            duration = data.get("duration")

            promo_code_amount = 0
            promo_code = None
            if promo_code_str:
                promo_code = db.session.query(PromoCode).filter_by(code=promo_code_str).first()
                if promo_code:
                    promo_code_amount = promo_code.amount

            price = total_amount - promo_code_amount

            subscription = Subscribe(
                name=plan.plan.name,
                start_date=datetime.now(),
                total_amount=total_amount,
                price=price,
                status="paid",
                service_plan_id=plan.id,
                duration_month=duration,
                promo_code_id=promo_code.id if promo_code else None,
            )
            db.session.add(subscription)
            db.session.flush()

            payment = payment = Payment(
                amount=price,
                payment_method=data.get("payment_method", "card"),
                subscription_id=subscription.id,
                profile_id=profile.id,
                status="pending",
            )

            db.session.add(payment)
            db.session.commit()

            payment_check = db.session.query(Payment).filter_by(id=payment.id).first()
            if not payment_check:
                return self.response_400(message="Payment ID not found in database")

            payment_service = PaymentService()
            payment_response = payment_service.post_payement(payment.id)[0]

            _logger.error(f"Payment service response: {payment_response}")

            if isinstance(payment_response, str):
                try:
                    import json

                    payment_response = json.loads(payment_response)
                except json.JSONDecodeError:
                    return self.response_500(message="Invalid payment service response format")

            if not isinstance(payment_response, dict):
                return self.response_500(message="Invalid payment service response")

            if "ERRORCODE" in payment_response and payment_response["ERRORCODE"] != 0:
                return self.response_400(
                    message="Payment failed",
                    error_code=payment_response.get("ERRORCODE"),
                    details=payment_response.get("ERRORMESSAGE", "Unknown error"),
                )

            payment.status = "completed"
            db.session.commit()

            return self.response(
                200,
                **{
                    "subscription": {
                        "id": subscription.id,
                        "name": subscription.name,
                        "start_date": subscription.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "total_amount": subscription.total_amount,
                        "price": subscription.price,
                        "status": subscription.status,
                        "duration_month": subscription.duration_month,
                        "service_plan_id": subscription.service_plan_id,
                        "promo_code_id": subscription.promo_code_id,
                    },
                    "order_id": payment_response.get("ORDER_ID"),
                    "form_url": payment_response.get("FORM_URL"),
                },
            )

        except Exception as e:
            _logger.error(f"Error in subscription: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")


appbuilder.add_api(SubscriptionApi)
