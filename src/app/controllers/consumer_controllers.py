# -*- coding: utf-8 -*-
import logging
import uuid
from flask import Response, jsonify
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required
from app import appbuilder, db
from app.models import Subscribe, Parameter, ParameterValue, Service
from app.services.apisix_service import ApiSixService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class ConsumerApi(BaseApi):
    resource_name = "my-service"

    @protect()
    @jwt_required()
    @expose("/<int:subscribe_id>/consumer", methods=["POST"])
    def create_my_service_consumer(self, subscribe_id):
        """
        Creates an API consumer for a given Subscribe ID and returns an API key.
        ---
        post:
          parameters:
            - in: path
              name: subscribe_id
              required: true
              schema:
                type: integer
              description: ID of the Subscribe to associate with the API consumer
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
              description: Subscribe not found
            500:
              description: Internal server error
        """
        user = get_user()

        subscribe = (
            db.session.query(Subscribe).filter(
                Subscribe.id == subscribe_id).first()
        )

        if not subscribe or not subscribe.service_plan:
            return Response("Subscribe or ServicePlan not found", status=400)

        service = subscribe.service_plan.service

        if not service:
            return Response("Service not found", status=400)

        param_value = (
            db.session.query(ParameterValue)
            .join(Parameter)
            .filter(ParameterValue.created_by == user)
            .filter(ParameterValue.subscribe_id == subscribe.id)
            .filter(Parameter.service_id == service.id, Parameter.type == "token")
            .first()
        )

        if param_value:
            api_key = param_value.value
        else:
            api_key = uuid.uuid4().hex[:32]

            parameter = (
                db.session.query(Parameter)
                .filter(Parameter.type == "token", Parameter.service_id == service.id)
                .first()
            )
            if not parameter:
                return Response("No valid Parameter of type 'token' found", status=400)

            new_param_value = ParameterValue(
                value=api_key,
                created_by=user,
                parameter_id=parameter.id,
                subscribe_id=subscribe.id,
            )
            print(
                f"Inserting new ParameterValue with subscribe_id={subscribe.id}")

            db.session.add(new_param_value)
            db.session.commit()

        try:
            consumer_username = f"subscribe_{subscribe_id}_user"
            apisix_service = ApiSixService()
            response = apisix_service.create_consumer(
                username=consumer_username,
                api_key=api_key,
                labels={"service": service.name},
            )

            return jsonify({"auth-key": api_key}), 200

        except Exception as e:
            _logger.error(f"Error creating API consumer: {e}", exc_info=True)
            return Response("Internal Server Error", status=500)


appbuilder.add_api(ConsumerApi)
