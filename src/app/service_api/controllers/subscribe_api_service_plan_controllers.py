import logging

from flask import request
from flask_appbuilder.api import BaseApi, expose, protect, rison
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.services.subscription_service import SubscriptionService
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
            subscription_service = SubscriptionService(db.session, _logger)

            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = subscription_service.validate_subscription_request(
                data
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate profile
            is_valid, error_msg, profile = subscription_service.validate_profile(
                user, request_data.profile_id
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate service plan
            is_valid, error_msg, plan = subscription_service.validate_service_plan(
                request_data.service_plan_selected_id, profile
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Calculate pricing
            total_amount = plan.price * request_data.duration
            promo_code, discount_amount = subscription_service.validate_promo_code(
                request_data.promo_code, total_amount
            )
            final_price = total_amount - discount_amount

            # Determine subscription status based on balance
            has_sufficient_balance = profile.balance >= final_price
            subscription_status = "active" if has_sufficient_balance else "inactive"

            # Create subscription
            subscription = subscription_service.create_api_subscription(
                plan=plan,
                duration=request_data.duration,
                total_amount=total_amount,
                price=final_price,
                promo_code=promo_code,
                profile_id=profile.id,
                status=subscription_status,
                api_key="",
            )

            # Initialize payment response variables
            satim_order_id = ""
            form_url = ""

            # Handle payment processing for insufficient balance
            if not has_sufficient_balance:
                payment = subscription_service.create_payment(
                    price=final_price,
                    payment_method=request_data.payment_method,
                    subscription_id=subscription.id,
                    profile_id=profile.id,
                )

                # Handle card payment for non-default profiles
                if request_data.payment_method == "card" and profile.profile_type != "default":
                    # # TODO Verify CAPTCHA
                    # is_valid, error_msg = subscription_service.verify_captcha(
                    #     request_data.captcha_token
                    # )
                    # if not is_valid:
                    #     return self.response_400(message=error_msg)

                    # Process payment
                    is_mvc_call = False
                    client_confirm_url = request_data.client_confirm_url
                    client_fail_url = request_data.client_fail_url

                    success, error_msg, payment_response = subscription_service.process_payment(
                        subscription, total_amount, is_mvc_call, client_confirm_url, client_fail_url
                    )
                    if not success:
                        return self.response_400(message=error_msg)

                    satim_order_id = payment_response.get("ORDER_ID", "")
                    form_url = payment_response.get("FORM_URL", "")
                    payment.satim_order_id = satim_order_id
                    payment.status = "completed"
                    db.session.commit()

            # Update promo code usage
            subscription_service.update_promo_code_usage(promo_code, subscription.id)

            # Send notification emails
            subscription_service.send_notification_emails(
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

    @expose("/upgrade", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def upgrade_api_subscription(self, **kwargs):
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
            # Initialize services
            subscription_service = SubscriptionService(db.session, _logger)

            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = subscription_service.validate_upgrade_request(data)
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate profile
            is_valid, error_msg, profile = subscription_service.validate_profile(
                user, request_data.profile_id
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate service plan
            is_valid, error_msg, plan = subscription_service.validate_service_plan(
                request_data.service_plan_selected_id, profile
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Calculate pricing
            total_amount = plan.price * request_data.duration
            promo_code, discount_amount = subscription_service.validate_promo_code(
                request_data.promo_code, total_amount
            )
            final_price = total_amount - discount_amount

            # Validate old subscription
            is_valid, error_msg, old_subscription = subscription_service.validate_old_subscription(
                request_data.old_subscription_id,
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            remaining_money = subscription_service.get_remaining_value(old_subscription)
            if remaining_money:
                final_price = final_price - remaining_money

            # Determine subscription status based on balance
            has_sufficient_balance = profile.balance >= final_price
            subscription_status = "active" if has_sufficient_balance else "inactive"

            # Create subscription
            subscription = subscription_service.create_api_subscription(
                plan=plan,
                duration=request_data.duration,
                total_amount=total_amount,
                price=final_price,
                promo_code=promo_code,
                profile_id=profile.id,
                status=subscription_status,
                api_key=old_subscription.api_key,
                is_upgrade=True,
            )

            # Initialize payment response variables
            satim_order_id = ""
            form_url = ""

            # Handle payment processing for insufficient balance
            if not has_sufficient_balance:
                payment = subscription_service.create_payment(
                    price=final_price,
                    payment_method=request_data.payment_method,
                    subscription_id=subscription.id,
                    profile_id=profile.id,
                )

                # Handle card payment for non-default profiles
                if request_data.payment_method == "card" and profile.profile_type != "default":

                    # Verify CAPTCHA
                    is_valid, error_msg = subscription_service.verify_captcha(
                        request_data.captcha_token
                    )
                    if not is_valid:
                        return self.response_400(message=error_msg)

                    # Process payment
                    is_mvc_call = False
                    client_confirm_url = request_data.client_confirm_url
                    client_fail_url = request_data.client_fail_url

                    success, error_msg, payment_response = subscription_service.process_payment(
                        subscription, total_amount, is_mvc_call, client_confirm_url, client_fail_url
                    )
                    if not success:
                        return self.response_400(message=error_msg)

                    satim_order_id = payment_response.get("ORDER_ID", "")
                    form_url = payment_response.get("FORM_URL", "")
                    payment.satim_order_id = satim_order_id
                    db.session.commit()

            # Update old subscrption
            subscription_service.update_old_subscription(old_subscription, is_upgrade=True)

            # Update promo code usage
            subscription_service.update_promo_code_usage(promo_code, subscription.id)

            # Send notification emails
            subscription_service.send_notification_emails(
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
    def renew_api_subscription(self, **kwargs):
        """Renew Subscription a user to a service plan.
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
            # Initialize services
            subscription_service = SubscriptionService(db.session, _logger)

            # Get and validate user
            user = get_user()
            if not user:
                return self.response_400(message="User not found")

            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = subscription_service.validate_renew_request(data)
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate profile
            is_valid, error_msg, profile = subscription_service.validate_profile(
                user, request_data.profile_id
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Validate old subscription
            is_valid, error_msg, old_subscription = subscription_service.validate_old_subscription(
                request_data.old_subscription_id,
            )
            if not is_valid:
                return self.response_400(message=error_msg)

            # Calculate pricing
            total_amount = old_subscription.service_plan.price * request_data.duration
            promo_code, discount_amount = subscription_service.validate_promo_code(
                request_data.promo_code, total_amount
            )
            final_price = total_amount - discount_amount

            remaining_money = subscription_service.get_remaining_value(old_subscription)
            if remaining_money:
                final_price = final_price - remaining_money

            # Determine subscription status based on balance
            has_sufficient_balance = profile.balance >= final_price
            subscription_status = "active" if has_sufficient_balance else "inactive"

            # Create subscription
            subscription = subscription_service.create_api_subscription(
                plan=old_subscription.service_plan,
                duration=request_data.duration,
                total_amount=total_amount,
                price=final_price,
                promo_code=promo_code,
                profile_id=profile.id,
                status=subscription_status,
                api_key=old_subscription.api_key,
                is_renew=True,
            )

            # Initialize payment response variables
            satim_order_id = ""
            form_url = ""

            # Handle payment processing for insufficient balance
            if not has_sufficient_balance:
                payment = subscription_service.create_payment(
                    price=final_price,
                    payment_method=request_data.payment_method,
                    subscription_id=subscription.id,
                    profile_id=profile.id,
                )

                # Handle card payment for non-default profiles
                if request_data.payment_method == "card" and profile.profile_type != "default":

                    # Verify CAPTCHA
                    is_valid, error_msg = subscription_service.verify_captcha(
                        request_data.captcha_token
                    )
                    if not is_valid:
                        return self.response_400(message=error_msg)

                    # Process payment
                    is_mvc_call = False
                    client_confirm_url = request_data.client_confirm_url
                    client_fail_url = request_data.client_fail_url

                    success, error_msg, payment_response = subscription_service.process_payment(
                        subscription, total_amount, is_mvc_call, client_confirm_url, client_fail_url
                    )
                    if not success:
                        return self.response_400(message=error_msg)

                    satim_order_id = payment_response.get("ORDER_ID", "")
                    form_url = payment_response.get("FORM_URL", "")
                    payment.satim_order_id = satim_order_id
                    db.session.commit()

            # Update old subscrption
            subscription_service.update_old_subscription(old_subscription, is_renew=True)

            # Update promo code usage
            subscription_service.update_promo_code_usage(promo_code, subscription.id)

            # Send notification emails
            subscription_service.send_notification_emails(
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

    # @expose("/upgrade", methods=["POST"])
    # @protect()
    # @rison()
    # @jwt_required()
    # def upgrade_api_subscription(self, **kwargs):
    #     """Subscription a user to a service plan.
    #     ---
    #     post:
    #         summary: Subscription a user to a service plan
    #         description: Creates a new subscription for the authenticated user.
    #         requestBody:
    #             required: true
    #             content:
    #                 application/json:
    #                     schema:
    #                         type: object
    #                         properties:
    #                             profile_id:
    #                                 type: integer
    #                                 description: ID of the user's profile
    #                             service_plan_selected_id:
    #                                 type: integer
    #                                 description: ID of the selected service plan
    #                             total_amount:
    #                                 type: number
    #                                 format: float
    #                                 description: Total amount before applying promo codes
    #                             promo_code:
    #                                 type: string
    #                                 nullable: true
    #                                 description: Promo code (if applicable)
    #                             duration:
    #                                 type: integer
    #                                 description: Duration of the subscription in months
    #                             payment_method:
    #                                 type: string
    #                                 description: Payment method (e.g., "card", "paypal")
    #                             captcha_token:
    #                                 type: string
    #                                 description: Google reCAPTCHA token
    #                             old_subscription_id:
    #                                 type: integer
    #                                 description: ID of the selected version app service
    #         responses:
    #             200:
    #                 description: Subscription successful
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 subscription:
    #                                     type: object
    #                                     properties:
    #                                         id:
    #                                             type: integer
    #                                         name:
    #                                             type: string
    #                                         start_date:
    #                                             type: string
    #                                             format: date-time
    #                                         total_amount:
    #                                             type: number
    #                                         price:
    #                                             type: number
    #                                         status:
    #                                             type: string
    #                                         duration_month:
    #                                             type: integer
    #                                         service_plan_id:
    #                                             type: integer
    #                                         promo_code_id:
    #                                             type: integer
    #                                             nullable: true
    #                                 order_id:
    #                                     type: string
    #                                 form_url:
    #                                     type: string
    #             400:
    #                 description: Bad request (invalid input)
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 error:
    #                                     type: string
    #                                 message:
    #                                     type: string
    #             404:
    #                 description: Resource not found (e.g., user, plan, or profile)
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 error:
    #                                     type: string
    #             500:
    #                 description: Internal server error
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 error:
    #                                     type: string
    #     """
    #     try:

    #         user = get_user()
    #         if not user:
    #             return self.response_400(message="User not found")
    #         data = request.get_json(silent=True)
    #         if not data:
    #             return self.response_400(message="Invalid request data")
    #         profile_id = data.get("profile_id")
    #         if not profile_id:
    #             return self.response_404(message="Profile id is required")
    #         profile = (
    #             db.session.query(PaymentProfile).filter_by(created_by=user, id=profile_id).first()
    #         )
    #         if not profile:
    #             return self.response_400(message="PaymentProfile not found")

    #         if profile.balance is None:
    #             return self.response_404(message="Insufficient balance")

    #         old_subscription_id = data.get("old_subscription_id")
    #         if not old_subscription_id:
    #             return self.response_404(message="old subscription id is required")

    #         plan_id = data.get("service_plan_selected_id")
    #         plan = db.session.query(ServicePlan).filter_by(id=plan_id).first()
    #         if not plan:
    #             return self.response_400(message="Service Plan not found")

    #         if profile.profile_type == "default":

    #             if plan and plan.service and not plan.service.is_eligible:
    #                 return self.response_400(
    #                     message="This service plan is not eligible for subscription"
    #                 )

    #         promo_code_str = data.get("promo_code")

    #         duration = data.get("duration")
    #         total_amount = plan.price * duration
    #         # code promo verification
    #         promo_code_amount = 0
    #         promo_code = None
    #         if promo_code_str:
    #             promo_code = (
    #                 db.session.query(PromoCode).filter_by(code=promo_code_str, active=True).first()
    #             )
    #             if promo_code and promo_code.is_valid:
    #                 promo_code_amount = (total_amount * promo_code.rate) / 100

    #         price = total_amount - promo_code_amount
    #         satim_order_id = ""
    #         form_url = ""

    #         subscription_template = render_template(
    #             "emails/deploily_subscription.html", user_name=user.username, plan=plan
    #         )

    #         # Todo get api key from old subscription
    #         _logger.info(f"######################################{old_subscription_id}")

    #         old_subscription = (
    #             db.session.query(ApiServiceSubscription).filter_by(id=old_subscription_id).first()
    #         )
    #         if not old_subscription:
    #             return self.response_400(message="old_subscription not found")

    #         remaining_money = self.get_remaining_value(old_subscription)
    #         if remaining_money:
    #             price = price - remaining_money
    #             print(price)
    #         # Balance verification
    #         # Case1: Sufficient balance
    #         if profile.balance - price >= 0:
    #             subscription = ApiServiceSubscription(
    #                 name=plan.plan.name,
    #                 start_date=datetime.now(),
    #                 total_amount=total_amount,
    #                 price=price,
    #                 service_plan_id=plan.id,
    #                 duration_month=duration,
    #                 promo_code_id=promo_code.id if promo_code else None,
    #                 status="active",
    #                 payment_status="paid",
    #                 profile_id=profile.id,
    #                 api_key=old_subscription.api_key,
    #             )
    #             db.session.add(subscription)
    #             db.session.commit()
    #             db.session.flush()
    #             email = Mail(
    #                 title=f"New Subscription Created by {user.username}",
    #                 body=subscription_template,
    #                 email_to=current_app.config["NOTIFICATION_EMAIL"],
    #                 email_from=current_app.config["NOTIFICATION_EMAIL"],
    #                 mail_state="outGoing",
    #             )
    #             db.session.add(email)
    #             db.session.commit()
    #             send_mail.delay(email.id)
    #             _logger.info(f"[EMAIL] is successfully sent for subscription {subscription.id}")

    #         else:  # Case2: unsufficient balance

    #             subscription = ApiServiceSubscription(
    #                 name=plan.plan.name,
    #                 start_date=datetime.now(),
    #                 total_amount=total_amount,
    #                 price=price,
    #                 service_plan_id=plan.id,
    #                 duration_month=duration,
    #                 promo_code_id=promo_code.id if promo_code else None,
    #                 status="inactive",
    #                 payment_status="unpaid",
    #                 profile_id=profile.id,
    #                 api_key=old_subscription.api_key,
    #             )

    #             db.session.add(subscription)
    #             db.session.flush()

    #             payment = Payment(
    #                 amount=price,
    #                 payment_method=data.get("payment_method", "card"),
    #                 subscription_id=subscription.id,
    #                 profile_id=profile.id,
    #                 status="pending",
    #             )
    #             db.session.add(payment)
    #             db.session.commit()
    #             email = Mail(
    #                 title=f"New Subscription Created by {user.username}",
    #                 body=subscription_template,
    #                 email_to=current_app.config["NOTIFICATION_EMAIL"],
    #                 email_from=current_app.config["NOTIFICATION_EMAIL"],
    #                 mail_state="outGoing",
    #             )
    #             db.session.add(email)
    #             db.session.commit()
    #             send_mail.delay(email.id)
    #             _logger.info(f"[EMAIL] is successfully sent for subscription {subscription.id}")
    #             if (
    #                 data.get("payment_method", "card") == "card"
    #                 and profile.profile_type != "default"
    #             ):
    #                 captcha_token = data.get("captcha_token")
    #                 if not captcha_token:
    #                     return self.response_400(message="Missing CAPTCHA token")
    #                 verify_url = "https://www.google.com/recaptcha/api/siteverify"
    #                 payload = {
    #                     "secret": current_app.config["CAPTCHA_SECRET_KEY"],
    #                     "response": captcha_token,
    #                 }
    #                 try:
    #                     captcha_response = requests.post(verify_url, data=payload)
    #                     captcha_result = captcha_response.json()
    #                 except Exception:
    #                     _logger.error("Failed to contact reCAPTCHA", exc_info=True)
    #                     return self.response_500(message="CAPTCHA verification error")

    #                 if not captcha_result.get("success"):
    #                     return self.response_400(message="CAPTCHA verification failed")

    #                 payment_check = db.session.query(Payment).filter_by(id=payment.id).first()
    #                 if not payment_check:
    #                     return self.response_400(message="Payment ID not found in database")
    #                 payment.order_id = "PAY" + str(payment.id)
    #                 db.session.commit()
    #                 payment_service = PaymentService()
    #                 payment_response = payment_service.post_payement(
    #                     payment.order_id, total_amount
    #                 )[0]

    #                 _logger.error(f"Payment service response: {payment_response}")

    #                 if isinstance(payment_response, str):
    #                     try:
    #                         import json

    #                         payment_response = json.loads(payment_response)
    #                     except json.JSONDecodeError:
    #                         return self.response_500(
    #                             message="Invalid payment service response format"
    #                         )

    #                 if not isinstance(payment_response, dict):
    #                     return self.response_500(message="Invalid payment service response")

    #                 if "ERROR_CODE" in payment_response and payment_response["ERROR_CODE"] != "0":
    #                     return self.response_400(
    #                         message="Payment failed",
    #                         # error_code=payment_response.get("ERROR_CODE"),
    #                         details=payment_response.get("ERROR_MESSAGE", "Unknown error"),
    #                     )
    #                 satim_order_id = payment_response.get("ORDER_ID")
    #                 form_url = payment_response.get("FORM_URL")

    #                 payment.satim_order_id = satim_order_id

    #                 db.session.commit()

    #         old_subscription.start_date = datetime.now() - relativedelta(
    #             months=old_subscription.duration_month + 1
    #         )
    #         old_subscription.status = "inactive"
    #         old_subscription.is_upgrade = True

    #         db.session.commit()
    #         if promo_code:
    #             if promo_code.usage_type == "single_use":
    #                 promo_code.active = False
    #                 promo_code.subscription = subscription.id
    #                 db.session.commit()
    #             else:
    #                 promo_code.subscription = subscription.id
    #                 db.session.commit()

    #         # Email to user
    #         subscription_template = render_template(
    #             "emails/user_subscription.html",
    #             user=user,
    #             service_name=plan.plan.name,
    #             total_price=total_amount,
    #         )
    #         email = Mail(
    #             title=f"Nouvelle souscription à deploily.cloud",
    #             body=subscription_template,
    #             email_to=user.email,
    #             email_from=current_app.config["NOTIFICATION_EMAIL"],
    #             mail_state="outGoing",
    #         )
    #         db.session.add(email)
    #         db.session.commit()
    #         send_mail.delay(email.id)

    #         return self.response(
    #             200,
    #             **{
    #                 "subscription": {
    #                     "id": subscription.id,
    #                     "name": subscription.name,
    #                     "start_date": subscription.start_date.strftime("%Y-%m-%d %H:%M:%S"),
    #                     "total_amount": subscription.total_amount,
    #                     "price": subscription.price,
    #                     "status": subscription.status,
    #                     "duration_month": subscription.duration_month,
    #                     "service_plan_id": subscription.service_plan_id,
    #                     "promo_code_id": subscription.promo_code_id,
    #                 },
    #                 "order_id": satim_order_id,
    #                 "form_url": form_url,
    #             },
    #         )

    #     except Exception as e:
    #         _logger.error(f"Error in subscription: {e}", exc_info=True)
    #         db.session.rollback()
    #         return self.response_500(message="Internal Server Error")

    # def get_remaining_value(self, old_subscription):
    #     total_price = old_subscription.price
    #     start_date = old_subscription.start_date
    #     duration_month = old_subscription.duration_month

    #     end_date = start_date + relativedelta(months=duration_month)
    #     today = datetime.now()

    #     # Ensure today is not beyond the end date
    #     if today > end_date:
    #         return 0.0

    #     total_days = (end_date - start_date).days
    #     used_days = (today - start_date).days
    #     print(used_days)
    #     remaining_days = total_days - used_days
    #     print(remaining_days)

    #     if total_days == 0:
    #         return 0.0

    #     remaining_value = (remaining_days / total_days) * total_price
    #     return round(remaining_value, 2)

    # @expose("/subscribe", methods=["POST"])
    # @protect()
    # @rison()
    # @jwt_required()
    # def subscribe_to_plan(self, **kwargs):
    #     """Subscription a user to a service plan.
    #     ---
    #     post:
    #         summary: Subscription a user to a service plan
    #         description: Creates a new subscription for the authenticated user.
    #         requestBody:
    #             required: true
    #             content:
    #                 application/json:
    #                     schema:
    #                         type: object
    #                         properties:
    #                             profile_id:
    #                                 type: integer
    #                                 description: ID of the user's profile
    #                             service_plan_selected_id:
    #                                 type: integer
    #                                 description: ID of the selected service plan
    #                             total_amount:
    #                                 type: number
    #                                 format: float
    #                                 description: Total amount before applying promo codes
    #                             promo_code:
    #                                 type: string
    #                                 nullable: true
    #                                 description: Promo code (if applicable)
    #                             duration:
    #                                 type: integer
    #                                 description: Duration of the subscription in months
    #                             payment_method:
    #                                 type: string
    #                                 description: Payment method (e.g., "card", "paypal")
    #                             captcha_token:
    #                                 type: string
    #                                 description: Google reCAPTCHA token
    #         responses:
    #             200:
    #                 description: Subscription successful
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 subscription:
    #                                     type: object
    #                                     properties:
    #                                         id:
    #                                             type: integer
    #                                         name:
    #                                             type: string
    #                                         start_date:
    #                                             type: string
    #                                             format: date-time
    #                                         total_amount:
    #                                             type: number
    #                                         price:
    #                                             type: number
    #                                         status:
    #                                             type: string
    #                                         duration_month:
    #                                             type: integer
    #                                         service_plan_id:
    #                                             type: integer
    #                                         promo_code_id:
    #                                             type: integer
    #                                             nullable: true
    #                                 order_id:
    #                                     type: string
    #                                 form_url:
    #                                     type: string
    #             400:
    #                 description: Bad request (invalid input)
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 error:
    #                                     type: string
    #                                 message:
    #                                     type: string
    #             404:
    #                 description: Resource not found (e.g., user, plan, or profile)
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 error:
    #                                     type: string
    #             500:
    #                 description: Internal server error
    #                 content:
    #                     application/json:
    #                         schema:
    #                             type: object
    #                             properties:
    #                                 error:
    #                                     type: string
    #     """
    #     try:

    #         user = get_user()
    #         if not user:
    #             return self.response_400(message="User not found")
    #         data = request.get_json(silent=True)
    #         if not data:
    #             return self.response_400(message="Invalid request data")
    #         profile_id = data.get("profile_id")
    #         if not profile_id:
    #             return self.response_404(message="Profile id is required")
    #         profile = (
    #             db.session.query(PaymentProfile).filter_by(created_by=user, id=profile_id).first()
    #         )
    #         if not profile:
    #             return self.response_400(message="PaymentProfile not found")

    #         if profile.balance is None:
    #             return self.response_404(message="Insufficient balance")

    #         plan_id = data.get("service_plan_selected_id")
    #         plan = db.session.query(ServicePlan).filter_by(id=plan_id).first()
    #         if not plan:
    #             return self.response_400(message="Service Plan not found")

    #         if profile.profile_type == "default":

    #             if plan and plan.service and not plan.service.is_eligible:
    #                 return self.response_400(
    #                     message="This service plan is not eligible for subscription"
    #                 )

    #         promo_code_str = data.get("promo_code")

    #         duration = data.get("duration")
    #         total_amount = plan.price * duration
    #         # code promo verification
    #         promo_code_amount = 0
    #         promo_code = None
    #         if promo_code_str:
    #             promo_code = (
    #                 db.session.query(PromoCode).filter_by(code=promo_code_str, active=True).first()
    #             )
    #             if promo_code and promo_code.is_valid:
    #                 promo_code_amount = (total_amount * promo_code.rate) / 100

    #         price = total_amount - promo_code_amount
    #         satim_order_id = ""
    #         form_url = ""

    #         subscription_template = render_template(
    #             "emails/deploily_subscription.html", user_name=user.username, plan=plan
    #         )
    #         # Balance verification
    #         # Case1: Sufficient balance
    #         if profile.balance - price >= 0:
    #             subscription = ApiServiceSubscription(
    #                 name=plan.plan.name,
    #                 start_date=datetime.now(),
    #                 total_amount=total_amount,
    #                 price=price,
    #                 service_plan_id=plan.id,
    #                 duration_month=duration,
    #                 promo_code_id=promo_code.id if promo_code else None,
    #                 status="active",
    #                 payment_status="paid",
    #                 profile_id=profile.id,
    #             )
    #             db.session.add(subscription)
    #             db.session.commit()
    #             db.session.flush()
    #             email = Mail(
    #                 title=f"New Subscription Created by {user.username}",
    #                 body=subscription_template,
    #                 email_to=current_app.config["NOTIFICATION_EMAIL"],
    #                 email_from=current_app.config["NOTIFICATION_EMAIL"],
    #                 mail_state="outGoing",
    #             )
    #             db.session.add(email)
    #             db.session.commit()
    #             send_mail.delay(email.id)
    #             _logger.info(f"[EMAIL] is successfully sent for subscription {subscription.id}")

    #         else:  # Case2: unsufficient balance

    #             subscription = ApiServiceSubscription(
    #                 name=plan.plan.name,
    #                 start_date=datetime.now(),
    #                 total_amount=total_amount,
    #                 price=price,
    #                 service_plan_id=plan.id,
    #                 duration_month=duration,
    #                 promo_code_id=promo_code.id if promo_code else None,
    #                 status="inactive",
    #                 payment_status="unpaid",
    #                 profile_id=profile.id,
    #             )

    #             db.session.add(subscription)
    #             db.session.flush()

    #             payment = Payment(
    #                 amount=price,
    #                 payment_method=data.get("payment_method", "card"),
    #                 subscription_id=subscription.id,
    #                 profile_id=profile.id,
    #                 status="pending",
    #             )
    #             db.session.add(payment)
    #             db.session.commit()
    #             email = Mail(
    #                 title=f"New Subscription Created by {user.username}",
    #                 body=subscription_template,
    #                 email_to=current_app.config["NOTIFICATION_EMAIL"],
    #                 email_from=current_app.config["NOTIFICATION_EMAIL"],
    #                 mail_state="outGoing",
    #             )
    #             db.session.add(email)
    #             db.session.commit()
    #             send_mail.delay(email.id)
    #             _logger.info(f"[EMAIL] is successfully sent for subscription {subscription.id}")
    #             if (
    #                 data.get("payment_method", "card") == "card"
    #                 and profile.profile_type != "default"
    #             ):
    #                 captcha_token = data.get("captcha_token")
    #                 if not captcha_token:
    #                     return self.response_400(message="Missing CAPTCHA token")
    #                 verify_url = "https://www.google.com/recaptcha/api/siteverify"
    #                 payload = {
    #                     "secret": current_app.config["CAPTCHA_SECRET_KEY"],
    #                     "response": captcha_token,
    #                 }
    #                 try:
    #                     captcha_response = requests.post(verify_url, data=payload)
    #                     captcha_result = captcha_response.json()
    #                 except Exception:
    #                     _logger.error("Failed to contact reCAPTCHA", exc_info=True)
    #                     return self.response_500(message="CAPTCHA verification error")

    #                 if not captcha_result.get("success"):
    #                     return self.response_400(message="CAPTCHA verification failed")

    #                 payment_check = db.session.query(Payment).filter_by(id=payment.id).first()
    #                 if not payment_check:
    #                     return self.response_400(message="Payment ID not found in database")
    #                 payment.order_id = "PAY" + str(payment.id)
    #                 db.session.commit()
    #                 payment_service = PaymentService()
    #                 payment_response = payment_service.post_payement(
    #                     payment.order_id, total_amount
    #                 )[0]

    #                 _logger.error(f"Payment service response: {payment_response}")

    #                 if isinstance(payment_response, str):
    #                     try:
    #                         import json

    #                         payment_response = json.loads(payment_response)
    #                     except json.JSONDecodeError:
    #                         return self.response_500(
    #                             message="Invalid payment service response format"
    #                         )

    #                 if not isinstance(payment_response, dict):
    #                     return self.response_500(message="Invalid payment service response")

    #                 if "ERROR_CODE" in payment_response and payment_response["ERROR_CODE"] != "0":
    #                     return self.response_400(
    #                         message="Payment failed",
    #                         # error_code=payment_response.get("ERROR_CODE"),
    #                         details=payment_response.get("ERROR_MESSAGE", "Unknown error"),
    #                     )
    #                 satim_order_id = payment_response.get("ORDER_ID")
    #                 form_url = payment_response.get("FORM_URL")

    #                 payment.satim_order_id = satim_order_id

    #                 db.session.commit()
    #         if promo_code:
    #             if promo_code.usage_type == "single_use":
    #                 promo_code.active = False
    #                 promo_code.subscription = subscription.id
    #                 db.session.commit()
    #             else:
    #                 promo_code.subscription = subscription.id
    #                 db.session.commit()

    #         # Email to user
    #         subscription_template = render_template(
    #             "emails/user_subscription.html",
    #             user=user,
    #             service_name=plan.plan.name,
    #             total_price=total_amount,
    #         )
    #         email = Mail(
    #             title=f"Nouvelle souscription à deploily.cloud",
    #             body=subscription_template,
    #             email_to=user.email,
    #             email_from=current_app.config["NOTIFICATION_EMAIL"],
    #             mail_state="outGoing",
    #         )
    #         db.session.add(email)
    #         db.session.commit()
    #         send_mail.delay(email.id)

    #         return self.response(
    #             200,
    #             **{
    #                 "subscription": {
    #                     "id": subscription.id,
    #                     "name": subscription.name,
    #                     "start_date": subscription.start_date.strftime("%Y-%m-%d %H:%M:%S"),
    #                     "total_amount": subscription.total_amount,
    #                     "price": subscription.price,
    #                     "status": subscription.status,
    #                     "duration_month": subscription.duration_month,
    #                     "service_plan_id": subscription.service_plan_id,
    #                     "promo_code_id": subscription.promo_code_id,
    #                 },
    #                 "order_id": satim_order_id,
    #                 "form_url": form_url,
    #             },
    #         )

    #     except Exception as e:
    #         _logger.error(f"Error in subscription: {e}", exc_info=True)
    #         db.session.rollback()
    #         return self.response_500(message="Internal Server Error")


appbuilder.add_api(SubscriptionApi)
