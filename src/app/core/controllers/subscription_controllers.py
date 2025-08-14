# -*- coding: utf-8 -*-

import logging

from flask import request
from flask_appbuilder.api import ModelRestApi, expose, protect
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
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
    "managed_ressource_id",
    "managed_ressource",
    "managed_ressource_details",
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
    "managed_ressource_details",
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

    def serialize_subscription(self, sub):
        """
        Custom serializer that handles related fields like service_plan.
        """
        return {
            "id": sub.id,
            "is_expired": sub.is_expired,
            "name": sub.name,
            "start_date": sub.start_date.isoformat() if sub.start_date else None,
            "total_amount": sub.total_amount,
            "price": sub.price,
            "payment_status": sub.payment_status,
            "duration_month": sub.duration_month,
            "status": sub.status,
            "service_plan_id": sub.service_plan.id if sub.service_plan else None,
            "service_plan": {
                "id": sub.service_plan.id,
                "price": sub.service_plan.price,
                "subscription_category": sub.service_plan.subscription_category,
            },
            "service_details": {
                "id": sub.service_details.get("id"),
                "name": sub.service_details.get("name"),
                "description": sub.service_details.get("description"),
                "documentation_url": sub.service_details.get("documentation_url"),
                "api_playground_url": sub.service_details.get("api_playground_url"),
                "unit_price": sub.service_details.get("unit_price"),
                "price_period": sub.service_details.get("price_period"),
                "service_url": sub.service_details.get("service_url"),
                "image_service": sub.service_details.get("image_service"),
                "short_description": sub.service_details.get("short_description"),
                "specifications": sub.service_details.get("specifications"),
                "curl_command": sub.service_details.get("curl_command"),
                "api_key": sub.service_details.get("api_key"),
                "is_subscribed": sub.service_details.get("is_subscribed"),
            },
            "managed_ressource_details": {
                "id": sub.managed_ressource_details.get("id"),
                "display_on_app": sub.managed_ressource_details.get("display_on_app"),
                "is_custom": sub.managed_ressource_details.get("is_custom"),
                "is_published": sub.managed_ressource_details.get("is_published"),
                "plan_id": sub.managed_ressource_details.get("plan_id"),
                "preparation_time": sub.managed_ressource_details.get("preparation_time"),
                "price": sub.managed_ressource_details.get("price"),
                "priority": sub.managed_ressource_details.get("priority"),
                "service_id": sub.managed_ressource_details.get("service_id"),
                "service_plan_type": sub.managed_ressource_details.get("service_plan_type"),
                "subscription_category": sub.managed_ressource_details.get("subscription_category"),
                "unity": sub.managed_ressource_details.get("unity"),
            },
            "promo_code_id": sub.promo_code.id if sub.promo_code else None,
            "promo_code_name": sub.promo_code.code if sub.promo_code else None,
            "api_key": sub.api_key,
            "is_encrypted": sub.is_encrypted,
            "profile_id": sub.profile.id if sub.profile else None,
            "profile_name": sub.profile.name if hasattr(sub.profile, "name") else None,
            "is_upgrade": sub.is_upgrade,
            "is_renew": sub.is_renew,
            "is_expired": sub.is_expired,
        }

    @expose("/history", methods=["GET"])
    @protect()
    def history(self):
        """
        ---
        get:
            summary: Get all expired subscriptions for the current user
            description: Returns a list of all expired subscriptions created by the authenticated user.
            parameters:
                - in: query
                  name: type
                  required: false
                  schema:
                    type: string
                  description: Filter by subscription type (e.g., "subscription_api_service")


            responses:
                200:
                    description: A list of subscriptions
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                    type: object
                401:
                    description: Unauthorized
                500:
                    description: Internal server error
        """
        user_id = get_user()
        if not user_id:
            return self.response(401, message="Unauthorized")

        # Get all subscriptions for the user
        query = (
            db.session.query(Subscription)
            .filter(Subscription.created_by == user_id)
            .order_by(Subscription.id.desc())
        )

        sub_type = request.args.get("type")  # Get type filter from query string

        if sub_type:
            query = query.filter(Subscription.type == sub_type)

        # Filter expired ones using the computed property
        expired_subs = [sub for sub in query.all() if sub.is_expired]

        # Serialize results using custom serializer
        results = [self.serialize_subscription(sub) for sub in expired_subs]

        return self.response(200, result=results)


appbuilder.add_api(SubscriptionModelApi)
