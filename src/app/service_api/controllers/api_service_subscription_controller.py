# -*- coding: utf-8 -*-

import logging
import re
import uuid

from flask import Response, jsonify
from flask_appbuilder.api import expose, protect
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.core.controllers.subscription_controllers import SubscriptionModelApi
from app.core.models.service_plan_option_models import ServicePlanOption
from app.service_api.models.api_service_subscription_model import ApiServiceSubscription
from app.service_api.models.api_services_model import ApiService
from app.services.apisix_service import ApiSixService
from app.utils.utils import get_user

# -*- coding: utf-8 -*-


_logger = logging.getLogger(__name__)


class ApiServiceSubscriptionModelApi(SubscriptionModelApi):
    resource_name = "api-service-subscription"
    datamodel = SQLAInterface(ApiServiceSubscription)

    add_columns = SubscriptionModelApi.add_columns
    list_columns = SubscriptionModelApi.list_columns
    show_columns = SubscriptionModelApi.show_columns
    edit_columns = SubscriptionModelApi.edit_columns
    # base_filters = [
    #     ["status", FilterEqual, "active"],
    #     ["is_upgrade", FilterEqual, False],
    #     ["is_renew", FilterEqual, False],
    # ]

    @protect()
    @jwt_required()
    @expose("/<int:subscribe_id>/token", methods=["POST"])
    def create_my_service_consumer(self, subscribe_id):
        """
        Creates an API consumer for a given Subscription ID and returns an API key.
        ---
        post:
          parameters:
            - in: path
              name: subscribe_id
              required: true
              schema:
                type: integer
              description: ID of the Subscription to associate with the API consumer
          responses:
            200:
              description: API consumer created successfully
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      auth-key:
                        type: string
                        description: Generated API key
            400:
              description: Subscription not found
            500:
              description: Internal server error
        """
        user = get_user()
        user_name = user.username
        slug_user_name = re.sub(r"[^a-zA-Z0-9]", "", user_name)

        subscribe = (
            db.session.query(ApiServiceSubscription)
            .filter(ApiServiceSubscription.id == subscribe_id)
            .first()
        )

        if not subscribe or not subscribe.service_plan:
            return Response("Subscription or ServicePlan not found", status=400)
        if subscribe.is_expired:
            return Response("Subscription is expired", status=400)

        base_service = subscribe.service_plan.service

        if not base_service:
            return Response("Service not found", status=400)

        plan_name = subscribe.service_plan.plan.name.lower()
        re.sub(r"[^a-zA-Z0-9]", "", plan_name)

        service = db.session.query(ApiService).filter(ApiService.id == base_service.id).first()
        api_key = uuid.uuid4().hex[:32]

        try:
            # consumer_username = f"{service.service_slug}_{slug_plan_name}_{slug_user_name}"
            consumer_username = f"{service.service_slug}_{slug_user_name}"
            apisix_service = ApiSixService()
            service_plan_option = (
                db.session.query(ServicePlanOption)
                .filter(
                    ServicePlanOption.option_type == "request_limit",
                    ServicePlanOption.service_plans.any(id=subscribe.service_plan.id),
                )
                .first()
            )
            if not service_plan_option:
                _logger.error(
                    f"No service plan option found for service plan {subscribe.service_plan.id}"
                )
                return Response("Service plan option not found", status=400)
            rate = service_plan_option.option_value
            if not rate or not isinstance(rate, int) or rate <= 0:
                _logger.error(
                    f"Invalid rate value for service plan option {service_plan_option.id}: {rate}"
                )
                return Response("Invalid rate value", status=400)
            limit_config = {
                "count": rate,
                "time_window": 1,
                "rejected_code": 429,
                "key": "consumer_name",
                "policy": "local",
            }
            response = apisix_service.create_consumer(
                username=consumer_username,
                api_key=api_key,
                limit_count=limit_config,
                labels={"service": service.service_slug},
                group_id=service.apisix_group_id,
            )
            if not response:
                _logger.error(f"Failed to create API consumer")
                return Response("Failed to create API consumer", status=500)
            subscribe.api_key = api_key
            db.session.commit()
            return jsonify({"auth-key": api_key}), 200

        except Exception as e:
            _logger.error(f"Error creating API consumer: {e}", exc_info=True)
            return Response("Internal Server Error", status=500)


appbuilder.add_api(ApiServiceSubscriptionModelApi)
