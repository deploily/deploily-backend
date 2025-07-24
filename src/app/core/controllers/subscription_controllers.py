# -*- coding: utf-8 -*-

import logging

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
            # "service_plan_name": sub.service_plan.name if sub.service_plan else None,
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

        # Filter expired ones using the computed property
        expired_subs = [sub for sub in query.all() if sub.is_expired]
        print("Expired Subscriptions:", expired_subs)

        # Serialize results using custom serializer
        results = [self.serialize_subscription(sub) for sub in expired_subs]

        return self.response(200, result=results)


appbuilder.add_api(SubscriptionModelApi)
