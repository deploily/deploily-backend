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
    # @expose("/<int:subscribe_id>/token", methods=["POST"])
    # def create_my_service_consumer(self, subscribe_id):
    #     """
    #     Creates an API consumer for a given Subscription ID and returns an API key.
    #     ---
    #     post:
    #       parameters:
    #         - in: path
    #           name: subscribe_id
    #           required: true
    #           schema:
    #             type: integer
    #           description: ID of the Subscription to associate with the API consumer
    #       responses:
    #         200:
    #           description: API consumer created successfully
    #           content:
    #             application/json:
    #               schema:
    #                 type: object
    #                 properties:
    #                   auth-key:
    #                     type: string
    #                     description: Generated API key
    #         400:
    #           description: Subscription not found
    #         500:
    #           description: Internal server error
    #     """
    #     user = get_user()
    #     user_name = user.username
    #     slug_user_name = re.sub(r"[^a-zA-Z0-9]", "", user_name)

    #     subscribe = db.session.query(Subscription).filter(Subscription.id == subscribe_id).first()

    #     if not subscribe or not subscribe.service_plan:
    #         return Response("Subscription or ServicePlan not found", status=400)

    #     service = subscribe.service_plan.service

    #     if not service:
    #         return Response("Service not found", status=400)

    #     if subscribe.api_key:
    #         api_key = subscribe.api_key
    #     else:
    #         api_key = uuid.uuid4().hex[:32]
    #         # subscribe.api_key = api_key
    #         # db.session.commit()

    #     try:
    #         consumer_username = f"{service.service_slug}_{slug_user_name}"
    #         apisix_service = ApiSixService()
    #         service_plan_option = (
    #             db.session.query(ServicePlanOption)
    #             .filter(
    #                 ServicePlanOption.option_type == "request_limit",
    #                 ServicePlanOption.service_plans.any(id=subscribe.service_plan.id),
    #             )
    #             .first()
    #         )
    #         if not service_plan_option:
    #             _logger.error(
    #                 f"No service plan option found for service plan {subscribe.service_plan.id}"
    #             )
    #             return Response("Service plan option not found", status=400)
    #         rate = service_plan_option.option_value
    #         if not rate or not isinstance(rate, int) or rate <= 0:
    #             _logger.error(
    #                 f"Invalid rate value for service plan option {service_plan_option.id}: {rate}"
    #             )
    #             return Response("Invalid rate value", status=400)
    #         limit_config = {
    #             "count": rate,
    #             "time_window": 1,
    #             "rejected_code": 429,
    #             "key": "consumer_name",
    #             "policy": "local",
    #         }
    #         response = apisix_service.create_consumer(
    #             username=consumer_username,
    #             api_key=api_key,
    #             limit_count=limit_config,
    #             labels={"service": service.service_slug},
    #         )
    #         if not response:
    #             _logger.error(f"Failed to create API consumer")
    #             return Response("Failed to create API consumer", status=500)
    #         subscribe.api_key = api_key
    #         db.session.commit()
    #         return jsonify({"auth-key": api_key}), 200

    #     except Exception as e:
    #         _logger.error(f"Error creating API consumer: {e}", exc_info=True)
    #         return Response("Internal Server Error", status=500)


appbuilder.add_api(SubscriptionModelApi)
