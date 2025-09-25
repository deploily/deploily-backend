import logging
import uuid

from flask import request
from flask_appbuilder.api import BaseApi, expose, protect, rison
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.services.subscription_docker_service import SubscriptionDockerDeploymentService
from app.services.subscription_service_base import SubscriptionServiceBase
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class DockerDeploymentSubscriptionApi(BaseApi):
    resource_name = "docker-deployment-service-subscription"

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

                                promo_code:
                                    type: string
                                    nullable: true
                                    description: Promo code (if applicable)
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
                                recommendation_app_service_id:
                                    type: integer
                                    description: ID of the selected recommendation app service
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
            # Initialize services
            # subscription_service = SubscriptionService(db.session, _logger)
            subscription_docker_deployment_service = SubscriptionDockerDeploymentService(
                db.session, _logger
            )

            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = (
                subscription_docker_deployment_service.validate_docker_deployment_subscription_request(
                    data
                )
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            subscription_service_base = SubscriptionServiceBase(db.session, _logger)

            is_valid, error_msg, subscription_json = (
                subscription_service_base.process_subscription_request(user, request_data)
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            api_secret_key = uuid.uuid4().hex[:32]
            user = get_user()
            user_name = user.username
            client_site_url = f"https://{user_name}-ttkepay.apps.depoloily.cloud"

            has_sufficient_balance = (
                subscription_json["profile"].balance >= subscription_json["price"]
            )
            subscription_status = "active" if has_sufficient_balance else "inactive"

            # Create subscription
            subscription = subscription_docker_deployment_service.create_docker_deployment_subscription(
                plan=subscription_json["plan"],
                # ressource_service_plan=ressource_plan.id,
                # managed_ressource=managed_ressource.id,
                duration=subscription_json["duration"],
                total_amount=subscription_json["total_amount"],
                price=subscription_json["price"],
                phone=subscription_json["phone"],
                promo_code=subscription_json["promo_code"],
                profile_id=subscription_json["profile"].id,
                status=subscription_status,
                # version_id=subscription_json["version_id"],
            )

            managed_ressource = subscription_service_base.get_or_create_managed_ressource(
                ressource_plan=subscription_json["ressource_plan"],
                managed_ressource=subscription_json["managed_ressource"],
                subscription=subscription,
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


appbuilder.add_api(DockerDeploymentSubscriptionApi)
