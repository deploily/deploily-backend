import logging
from datetime import datetime

import requests
from flask import current_app, render_template, request
from flask_appbuilder.api import BaseApi, expose, protect, rison
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.core.celery_tasks.send_mail_task import send_mail
from app.core.models import Payment, PaymentProfile, PromoCode, ServicePlan
from app.core.models.mail_models import Mail
from app.service_apps.models.ttk_epay_subscription_model import (
    TtkEpaySubscriptionAppService,
)
from app.services.payment_service import PaymentService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class TtkEpaySubscriptionApi(BaseApi):
    resource_name = "ttk-epay-app-service-subscription"

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
                                recommendation_app_service_id:
                                    type: integer
                                    description: ID of the selected recommendation app service




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
            data = request.get_json(silent=True)
            if not data:
                return self.response_400(message="Invalid request data")
            profile_id = data.get("profile_id")
            if not profile_id:
                return self.response_404(message="Profile id is required")
            profile = (
                db.session.query(PaymentProfile).filter_by(created_by=user, id=profile_id).first()
            )
            if not profile:
                return self.response_400(message="PaymentProfile not found")

            if profile.balance is None:
                return self.response_404(message="Insufficient balance")

            plan_id = data.get("service_plan_selected_id")
            plan = db.session.query(ServicePlan).filter_by(id=plan_id).first()
            ressource_plan_id = data.get("ressource_service_plan_selected_id")
            ressource_plan = db.session.query(ServicePlan).filter_by(id=ressource_plan_id).first()

            if profile.profile_type == "default":

                if plan and plan.service and not plan.service.is_eligible:
                    return self.response_400(
                        message="This service plan is not eligible for subscription"
                    )

            # todo add new logic here
            if not plan:
                return self.response_400(message="Service Plan not found")

            promo_code_str = data.get("promo_code")
            duration = data.get("duration")
            total_amount = plan.price * duration
            if ressource_plan:
                total_amount += ressource_plan.price * duration

            # code promo verification
            promo_code_amount = 0
            promo_code = None
            if promo_code_str:
                promo_code = (
                    db.session.query(PromoCode).filter_by(code=promo_code_str, active=True).first()
                )

                if promo_code and promo_code.is_valid:
                    promo_code_amount = (total_amount * promo_code.rate) / 100

            # price = total_amount - promo_code_amount
            price = total_amount - promo_code_amount
            satim_order_id = ""
            form_url = ""

            subscription_template = render_template(
                "emails/deploily_subscription.html", user_name=user.username, plan=plan
            )
            # Balance verification
            # Case1: Sufficient balance
            if profile.balance - price >= 0:
                # todo add new logic here

                subscription = TtkEpaySubscriptionAppService(
                    name=plan.plan.name,
                    start_date=datetime.now(),
                    total_amount=total_amount,
                    price=price,
                    service_plan_id=plan.id,
                    duration_month=duration,
                    # application_status="processing",
                    promo_code_id=promo_code.id if promo_code else None,
                    status="active",
                    payment_status="paid",
                    profile_id=profile.id,
                )
                db.session.add(subscription)
                db.session.commit()
                db.session.flush()
                email = Mail(
                    title=f"New Subscription Created by {user.username}",
                    body=subscription_template,
                    email_to=current_app.config["NOTIFICATION_EMAIL"],
                    email_from=current_app.config["NOTIFICATION_EMAIL"],
                    mail_state="outGoing",
                )
                db.session.add(email)
                db.session.commit()
                send_mail.delay(email.id)
                _logger.info(f"[EMAIL] is successfully sent for subscription {subscription.id}")

            else:  # Case2: unsufficient balance

                subscription = TtkEpaySubscriptionAppService(
                    name=plan.plan.name,
                    start_date=datetime.now(),
                    total_amount=total_amount,
                    price=price,
                    service_plan_id=plan.id,
                    duration_month=duration,
                    promo_code_id=promo_code.id if promo_code else None,
                    status="inactive",
                    # application_status="processing",
                    payment_status="unpaid",
                    profile_id=profile.id,
                )

                db.session.add(subscription)
                db.session.flush()

                payment = Payment(
                    amount=price,
                    payment_method=data.get("payment_method", "card"),
                    subscription_id=subscription.id,
                    profile_id=profile.id,
                    status="pending",
                )
                db.session.add(payment)
                db.session.commit()
                email = Mail(
                    title=f"New Subscription Created by {user.username}",
                    body=subscription_template,
                    email_to=current_app.config["NOTIFICATION_EMAIL"],
                    email_from=current_app.config["NOTIFICATION_EMAIL"],
                    mail_state="outGoing",
                )
                db.session.add(email)
                db.session.commit()
                send_mail.delay(email.id)
                _logger.info(f"[EMAIL] is successfully sent for subscription {subscription.id}")
                if (
                    data.get("payment_method", "card") == "card"
                    and profile.profile_type != "default"
                ):
                    captcha_token = data.get("captcha_token")
                    if not captcha_token:
                        return self.response_400(message="Missing CAPTCHA token")
                    verify_url = "https://www.google.com/recaptcha/api/siteverify"
                    payload = {
                        "secret": current_app.config["CAPTCHA_SECRET_KEY"],
                        "response": captcha_token,
                    }
                    try:
                        captcha_response = requests.post(verify_url, data=payload)
                        captcha_result = captcha_response.json()
                    except Exception:
                        _logger.error("Failed to contact reCAPTCHA", exc_info=True)
                        return self.response_500(message="CAPTCHA verification error")

                    if not captcha_result.get("success"):
                        return self.response_400(message="CAPTCHA verification failed")

                    payment_check = db.session.query(Payment).filter_by(id=payment.id).first()
                    if not payment_check:
                        return self.response_400(message="Payment ID not found in database")
                    payment.order_id = "PAY" + str(payment.id)
                    db.session.commit()
                    payment_service = PaymentService()
                    payment_response = payment_service.post_payement(
                        payment.order_id, total_amount
                    )[0]

                    _logger.error(f"Payment service response: {payment_response}")

                    if isinstance(payment_response, str):
                        try:
                            import json

                            payment_response = json.loads(payment_response)
                        except json.JSONDecodeError:
                            return self.response_500(
                                message="Invalid payment service response format"
                            )

                    if not isinstance(payment_response, dict):
                        return self.response_500(message="Invalid payment service response")

                    if "ERROR_CODE" in payment_response and payment_response["ERROR_CODE"] != "0":
                        return self.response_400(
                            message="Payment failed",
                            # error_code=payment_response.get("ERROR_CODE"),
                            details=payment_response.get("ERROR_MESSAGE", "Unknown error"),
                        )
                    satim_order_id = payment_response.get("ORDER_ID")
                    form_url = payment_response.get("FORM_URL")

                    payment.satim_order_id = satim_order_id

                    db.session.commit()

            if promo_code:
                if promo_code.usage_type == "single_use":
                    promo_code.active = False
                    promo_code.subscription = subscription.id
                    db.session.commit()
                else:
                    promo_code.subscription = subscription.id
                    db.session.commit()

            # Email to user
            subscription_template = render_template(
                "emails/user_subscription.html",
                user=user,
                service_name=plan.plan.name,
                total_price=total_amount,
            )
            email = Mail(
                title=f"Nouvelle souscription à deploily.cloud",
                body=subscription_template,
                email_to=user.email,
                email_from=current_app.config["NOTIFICATION_EMAIL"],
                mail_state="outGoing",
            )
            db.session.add(email)
            db.session.commit()
            send_mail.delay(email.id)

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


appbuilder.add_api(TtkEpaySubscriptionApi)
