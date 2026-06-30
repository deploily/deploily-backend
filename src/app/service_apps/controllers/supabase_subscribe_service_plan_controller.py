import logging

from flask import request
from flask_appbuilder.api import BaseApi, expose, protect, rison
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.services.subscription_service_base import SubscriptionServiceBase
from app.services.subscription_supabase_service import SubscriptionSupabaseService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class SupabaseSubscriptionApi(BaseApi):
    resource_name = "supabase-app-service-subscription"

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


                                phone:
                                    type: string
                                    description: Phone number of the user
                                provider_name:
                                    type: string
                                    description: Provider name

                                duration:
                                    type: integer
                                    description: Duration of the subscription in months
                                payment_method:
                                    type: string
                                    description: Payment method (e.g., "card", "paypal")
                                captcha_token:
                                    type: string
                                    description: Google reCAPTCHA token

                                ressource_service_plan_selected_id:
                                    type: integer
                                    description: ID of the selected ressource service plan
                                managed_ressource_id:
                                    type: integer
                                    description: ID of the selected managed ressource
                                byor:
                                    type: boolean
                                    description: Whether it's a Bring Your Own Ressource subscription

                                is_trial:
                                    type: boolean
                                    description: Whether it's a trial subscription

                                recommendation_app_service_id:
                                    type: integer
                                    description: ID of the selected recommendation app service
                                version_selected_id:
                                    type: integer
                                    description: ID of the selected version app service
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

                                            price:
                                                type: number
                                            status:
                                                type: string
                                            duration_month:
                                                type: integer
                                            service_plan_id:
                                                type: integer

                                            ressource_service_plan_selected_id:
                                                type: integer
                                                description: ID of the selected ressource service plan
                                            managed_ressource_id:
                                                type: integer
                                                description: ID of the selected managed ressource
                                            byor:
                                                type: boolean
                                                description: Whether it's a Bring Your Own Ressource subscription

                                            recommendation_app_service_id:
                                                type: integer
                                                description: ID of the selected recommendation app service
                                            version_selected_id:
                                                type: integer
                                                description: ID of the selected version app service

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
            subscription_supabase_service = SubscriptionSupabaseService(db.session, _logger)

            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = (
                subscription_supabase_service.validate_supabase_subscription_request(data)
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
            subscription = subscription_supabase_service.create_supabase_subscription(
                plan=subscription_json["plan"],
                ressource_plan=subscription_json["ressource_plan"],
                managed_ressource=subscription_json["managed_ressource"],
                byor=request_data.byor if hasattr(request_data, "byor") else False,
                is_trial=(
                    subscription_json["is_trial"] if "is_trial" in subscription_json else False
                ),
                duration=subscription_json["duration"],
                total_amount=subscription_json["total_amount"],
                price=subscription_json["price"],
                profile_id=subscription_json["profile"].id,
                status=subscription_status,
                version_id=subscription_json["version_id"],
                phone=subscription_json["phone"],
                provider_name=subscription_json["provider_name"],
                tva_rate=subscription_json.get("tva_rate", 0.0),
                tva_amount=subscription_json.get("tva_amount", 0.0),
            )

            if not subscription_json["plan"].is_trial:

                success, error_msg, result = subscription_service_base.handle_payment_process(
                    user, subscription, request_data, has_sufficient_balance
                )
                if not success:
                    return self.response_400(message=error_msg)

                return self.response(200, **result, message="Payment processed successfully")
            else:
                # For trial subscriptions, return success response without payment processing
                db.session.commit()
                subscription_service_base.send_notification_emails(
                    user,
                    subscription_json["plan"],
                    subscription_json["total_amount"],
                    subscription,
                    request_data.payment_method,
                )

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
                        },
                        "order_id": None,
                        "form_url": None,
                    },
                    message="Trial subscription created successfully",
                )

        except Exception as e:
            _logger.error(f"Error in subscription: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")


appbuilder.add_api(SupabaseSubscriptionApi)
