# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.subscription_models import Subscription
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)
_subscribe_display_columns = [
    "id",
    "start_date",
    "total_amount",
    "price",
    "duration_month",
    "name",
    "status",
    "service_plan",
    "service_details",
    "api_key",
    "service_plan_id",
    "is_expired",
]

_subscribe_edit_columns = [
    "id",
    "start_date",
    "total_amount",
    "price",
    "duration_month",
    "name",
    "status",
    "service_plan",
    "api_key",
    "service_plan_id",
]


class SubscriptionModelApi(ModelRestApi):
    resource_name = "subscription"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Subscription)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = _subscribe_display_columns
    list_columns = _subscribe_display_columns
    show_columns = _subscribe_display_columns
    # edit_columns = [col for col in _subscribe_display_columns if col != "is_expired"]
    edit_columns = _subscribe_edit_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]

    # @protect()
    # @jwt_required()
    # @expose("/upgrade", methods=["POST"])
    # def upgrade_subscription(self):

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
    #                             subscription_id:
    #                                 type: integer
    #                                 description: ID of the user's profile
    #                             service_plan_selected_id:
    #                                 type: integer
    #                                 description: ID of the selected service plan

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
    #                             profile_id:
    #                                 type: integer
    #                                 description: ID of the user's profile
    #         responses:
    #             200:
    #                 description: Subscription upgraded successfully
    #             400:
    #                 description: Bad request
    #             500:
    #                 description: Internal server error

    #     """
    #     try:
    #         user = get_user()
    #         if not user:
    #             return self.response_400(message="User not found")
    #         data = request.get_json(silent=True)
    #         if not data:
    #             return self.response_400(message="Invalid request data")
    #         subscription_id = data.get("subscription_id")
    #         if not subscription_id:
    #             return self.response_404(message="subscription_id is required")
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

    #         if profile.profile_type == "default":

    #             if plan and plan.service and not plan.service.is_eligible:
    #                 return self.response_400(
    #                     message="This service plan is not eligible for subscription"
    #                 )

    #         service_plan_selected_id = data.get("service_plan_selected_id")
    #         if not service_plan_selected_id:
    #             return self.response_404(message="service_plan_selected_id is required")

    #         plan_id = data.get("service_plan_selected_id")
    #         plan = db.session.query(ServicePlan).filter_by(id=plan_id).first()
    #         if not plan:
    #             return self.response_400(message="Service Plan not found")

    #         promo_code_str = data.get("promo_code")
    #         duration = data.get("duration")
    #         total_amount = plan.price * duration

    #         promo_code_amount = 0
    #         promo_code = None
    #         if promo_code_str:
    #             promo_code = (
    #                 db.session.query(PromoCode).filter_by(code=promo_code_str, active=True).first()
    #             )

    #             if promo_code and promo_code.is_valid:
    #                 promo_code_amount = (total_amount * promo_code.rate) / 100

    #         # price = total_amount - promo_code_amount
    #         price = total_amount - promo_code_amount
    #         #TODO New logic

    #         old_subscription=  db.session.query(Subscription).filter_by(id=subscription_id).first()
    #         api_key=old_subscription.api_key
    #         old_subscription.is_expired=True
    #         db.commit

    #         #Todo create new consumer

    #     except Exception as e:
    #         return jsonify({"error": "Internal server error", "details": str(e)}), 500


appbuilder.add_api(SubscriptionModelApi)
