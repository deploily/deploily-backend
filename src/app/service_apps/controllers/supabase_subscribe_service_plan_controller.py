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
                                            promo_code_id:
                                                type: integer
                                                nullable: true
                                            ressource_service_plan_selected_id:
                                                type: integer
                                                description: ID of the selected ressource service plan
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

            # Create subscription
            subscription = subscription_supabase_service.create_supabase_subscription(
                plan=subscription_json["plan"],
                duration=subscription_json["duration"],
                total_amount=subscription_json["total_amount"],
                price=subscription_json["price"],
                promo_code=subscription_json["promo_code"],
                profile_id=subscription_json["profile"].id,
                status=subscription_json["status"],
                version_id=subscription_json["version_id"],
            )
            managed_ressource = subscription_service_base.get_or_create_managed_ressource(
                ressource_plan=subscription_json["ressource_plan"],
                managed_ressource=subscription_json["managed_ressource"],
                subscription=subscription,
            )

            success, error_msg, result = subscription_service_base.handle_payment_process(
                user, subscription, request_data, subscription_json["has_sufficient_balance"]
            )
            if not success:
                return self.response_400(message=error_msg)

            return self.response(200, data=result, message="Payment processed successfully")

        except Exception as e:
            _logger.error(f"Error in subscription: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")

    @expose("/upgrade", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def upgrade_app_subscription(self, **kwargs):
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
                                version_selected_id:
                                    type: integer
                                    description: ID of the selected version app service
                                old_subscription_id:
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
                                            promo_code_id:
                                                type: integer
                                                nullable: true
                                            ressource_service_plan_selected_id:
                                                type: integer
                                                description: ID of the selected ressource service plan
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
            subscription_service_base = SubscriptionServiceBase(db.session, _logger)
            subscription_supabase_service = SubscriptionSupabaseService(db.session, _logger)

            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = (
                subscription_supabase_service.validate_upgrade_supabase_subscription_request(data)
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate profile
            is_valid, error_msg, profile = subscription_service_base.validate_profile(
                user, request_data.profile_id
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate service plan
            is_valid, error_msg, plan = subscription_service_base.validate_service_plan(
                request_data.service_plan_selected_id, profile
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            if request_data.ressource_service_plan_selected_id is None:
                ressource_plan = None
            else:
                is_valid, error_msg, ressource_plan = (
                    subscription_service_base.validate_ressource_service_plan(
                        request_data.ressource_service_plan_selected_id
                    )
                )
                if not is_valid:
                    return self.response_400(message=error_msg)

            #  Validate managed ressource
            if request_data.managed_ressource_id is None:
                managed_ressource = None
            else:
                is_valid, error_msg, managed_ressource = (
                    subscription_service_base.validate_managed_ressource(
                        request_data.managed_ressource_id
                    )
                )
                if not is_valid:
                    return self.response_400(message=error_msg)

            # Validate service plan
            is_valid, error_msg, version = subscription_service_base.validate_version(
                request_data.version_selected_id
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Calculate pricing
            total_amount = plan.price * request_data.duration
            if ressource_plan:
                total_amount += ressource_plan.price * request_data.duration

            promo_code, discount_amount = subscription_service_base.validate_promo_code(
                request_data.promo_code, total_amount
            )
            final_price = total_amount - discount_amount

            # Validate old subscription
            is_valid, error_msg, old_subscription = (
                subscription_supabase_service.validate_old_supabase_subscription(
                    request_data.old_subscription_id,
                )
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            remaining_money = subscription_service_base.get_remaining_value(old_subscription)
            if remaining_money:
                final_price = final_price - remaining_money

            # Determine subscription status based on balance
            has_sufficient_balance = profile.balance >= final_price
            subscription_status = "active" if has_sufficient_balance else "inactive"

            # Create subscription
            subscription = subscription_supabase_service.create_supabase_subscription(
                plan=plan,
                duration=request_data.duration,
                total_amount=total_amount,
                price=final_price,
                promo_code=promo_code,
                profile_id=profile.id,
                status=subscription_status,
                version_id=version.id,
                # ressource_service_plan=ressource_plan.id,
                is_upgrade=True,
            )

            managed_ressource = subscription_service_base.get_or_create_managed_ressource(
                ressource_plan=ressource_plan,
                managed_ressource=managed_ressource,
                subscription=subscription,
            )

            # Initialize payment response variables
            satim_order_id = ""
            form_url = ""

            # Handle payment processing for insufficient balance
            if not has_sufficient_balance:
                payment = subscription_service_base.create_payment(
                    price=final_price,
                    payment_method=request_data.payment_method,
                    subscription_id=subscription.id,
                    profile_id=profile.id,
                )

                # Handle card payment for non-default profiles
                if request_data.payment_method == "card" and profile.profile_type != "default":

                    # Verify CAPTCHA
                    is_valid, error_msg = subscription_service_base.verify_captcha(
                        request_data.captcha_token
                    )
                    if not is_valid:
                        return self.response_400(message=error_msg)

                    # Process payment
                    is_mvc_call = False
                    client_confirm_url = request_data.client_confirm_url
                    client_fail_url = request_data.client_fail_url

                    success, error_msg, payment_response = (
                        subscription_service_base.process_payment(
                            subscription,
                            total_amount,
                            is_mvc_call,
                            client_confirm_url,
                            client_fail_url,
                        )
                    )
                    if not success:
                        return self.response_400(message=error_msg)

                    satim_order_id = payment_response.get("ORDER_ID", "")
                    form_url = payment_response.get("FORM_URL", "")
                    payment.satim_order_id = satim_order_id
                    db.session.commit()
            # Update old subscrption
            subscription_service_base.update_old_subscription(old_subscription, is_upgrade=True)

            # Update promo code usage
            subscription_service_base.update_promo_code_usage(promo_code, subscription.id)

            # Send notification emails
            subscription_service_base.send_notification_emails(
                user, plan, total_amount, subscription, request_data.payment_method
            )

            # Commit transaction
            db.session.commit()

            # Return success response
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
                    "order_id": satim_order_id,
                    "form_url": form_url,
                },
            )

        except Exception as e:
            _logger.error(f"Error in subscription: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")

    @expose("/renew", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def renew_app_subscription(self, **kwargs):
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

                                old_subscription_id:
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
            subscription_service_base = SubscriptionServiceBase(db.session, _logger)
            subscription_supabase_service = SubscriptionSupabaseService(db.session, _logger)

            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = (
                subscription_supabase_service.validate_supabase_renew_request(data)
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate profile
            is_valid, error_msg, profile = subscription_service_base.validate_profile(
                user, request_data.profile_id
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate old subscription
            is_valid, error_msg, old_subscription = (
                subscription_supabase_service.validate_old_supabase_subscription(
                    request_data.old_subscription_id,
                )
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Calculate pricing
            total_amount = old_subscription.service_plan.price * request_data.duration

            promo_code, discount_amount = subscription_service_base.validate_promo_code(
                request_data.promo_code, total_amount
            )
            final_price = total_amount - discount_amount

            remaining_money = subscription_service_base.get_remaining_value(old_subscription)
            if remaining_money:
                final_price = final_price - remaining_money

            # Determine subscription status based on balance
            has_sufficient_balance = profile.balance >= final_price
            subscription_status = "active" if has_sufficient_balance else "inactive"

            # Create subscription
            subscription = subscription_supabase_service.create_supabase_subscription(
                plan=old_subscription.service_plan,
                duration=request_data.duration,
                total_amount=total_amount,
                price=final_price,
                promo_code=promo_code,
                profile_id=profile.id,
                status=subscription_status,
                is_renew=True,
                version_id=old_subscription.version_id,
                # ressource_service_plan=old_subscription.ressource_service_plan_id,
            )
            subscription.managed_ressource_id = old_subscription.managed_ressource_id
            db.session.commit()

            # Initialize payment response variables
            satim_order_id = ""
            form_url = ""

            # Handle payment processing for insufficient balance
            if not has_sufficient_balance:
                payment = subscription_service_base.create_payment(
                    price=final_price,
                    payment_method=request_data.payment_method,
                    subscription_id=subscription.id,
                    profile_id=profile.id,
                )

                # Handle card payment for non-default profiles
                if request_data.payment_method == "card" and profile.profile_type != "default":

                    # Verify CAPTCHA
                    is_valid, error_msg = subscription_service_base.verify_captcha(
                        request_data.captcha_token
                    )
                    if not is_valid:
                        return self.response_400(message=error_msg)

                    # Process payment
                    is_mvc_call = False
                    client_confirm_url = request_data.client_confirm_url
                    client_fail_url = request_data.client_fail_url

                    success, error_msg, payment_response = (
                        subscription_service_base.process_payment(
                            subscription,
                            total_amount,
                            is_mvc_call,
                            client_confirm_url,
                            client_fail_url,
                        )
                    )
                    if not success:
                        return self.response_400(message=error_msg)

                    satim_order_id = payment_response.get("ORDER_ID", "")
                    form_url = payment_response.get("FORM_URL", "")
                    payment.satim_order_id = satim_order_id
                    db.session.commit()
            # Update old subscrption
            subscription_service_base.update_old_subscription(old_subscription, is_upgrade=True)

            # Update promo code usage
            subscription_service_base.update_promo_code_usage(promo_code, subscription.id)

            # Send notification emails
            subscription_service_base.send_notification_emails(
                user,
                old_subscription.service_plan,
                total_amount,
                subscription,
                request_data.payment_method,
            )

            # Commit transaction
            db.session.commit()

            # Return success response
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
                    "order_id": satim_order_id,
                    "form_url": form_url,
                },
            )

        except Exception as e:
            _logger.error(f"Error in subscription: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")


appbuilder.add_api(SupabaseSubscriptionApi)
