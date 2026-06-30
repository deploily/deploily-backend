import logging

from flask import request
from flask_appbuilder.api import BaseApi, expose, protect, rison
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.services.subscription_api_service import ApiSubscriptionService
from app.services.subscription_service_base import SubscriptionServiceBase
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class SubscriptionApi(BaseApi):
    resource_name = "api-service-subscription"

    @expose("/subscribe", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def subscribe_to_plan(self, **kwargs):
        """Subscription a user to a service plan.
        ---
        post:
            summary: Subscription a user to a service plan
            description: Creates a new subscription for the authenticated user.
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
                                service_plan_selected_id:
                                    type: integer
                                    description: ID of the selected service plan
                                total_amount:
                                    type: number
                                    format: float
                                    description: Total amount before applying promo codes

                                duration:
                                    type: integer
                                    description: Duration of the subscription in months
                                phone:
                                    type: string
                                    description: User's phone number
                                payment_method:
                                    type: string
                                    description: Payment method (e.g., "card", "paypal")
                                captcha_token:
                                    type: string
                                    description: Google reCAPTCHA token
                                client_confirm_url:
                                    type: string
                                    description: URL to redirect after confirmation
                                client_fail_url:
                                    type: string
                                    description: URL to redirect after failure
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
            # Initialize services
            api_subscription_service = ApiSubscriptionService(db.session, _logger)
            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = (
                api_subscription_service.validate_api_subscription_request(data)
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            subscription_service_base = SubscriptionServiceBase(db.session, _logger)

            is_valid, error_msg, subscription_json = (
                subscription_service_base.process_subscription_request(user, request_data)
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            has_sufficient_balance = (
                subscription_json["profile"].balance >= subscription_json["price"]
            )
            subscription_status = "active" if has_sufficient_balance else "inactive"

            # Create subscription
            subscription = api_subscription_service.create_api_subscription(
                plan=subscription_json["plan"],
                duration=subscription_json["duration"],
                total_amount=subscription_json["total_amount"],
                price=subscription_json["price"],
                profile_id=subscription_json["profile"].id,
                status=subscription_status,
                api_key="",
                phone=subscription_json["phone"],
            )

            success, error_msg, result = subscription_service_base.handle_payment_process(
                user, subscription, request_data, has_sufficient_balance
            )
            if not success:
                return self.response_400(message=error_msg)

            return self.response(200, **result, message="Payment processed successfully")

        except Exception as e:
            _logger.error(f"Error in subscription: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")


appbuilder.add_api(SubscriptionApi)
