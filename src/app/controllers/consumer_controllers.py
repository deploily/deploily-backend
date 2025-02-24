# -*- coding: utf-8 -*-

import logging
import secrets
from datetime import datetime
from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required
from flask_appbuilder.api import BaseApi, expose, protect
from app import db, appbuilder
from app.utils.utils import get_user
from app.models import CartLine, ParameterValue, Parameter, Service
from app.services.apisix_service import ApiSixService

_logger = logging.getLogger(__name__)


class ConsumerApi(BaseApi):
    resource_name = "consumer"

    @protect()
    @jwt_required()
    @expose("/cart-line/<int:cart_line_id>", methods=["POST"])
    def create_cart_line_consumer(self, cart_line_id):
        """
        Creates an API consumer for a given CartLine ID and returns an API key.
        ---
        post:
          parameters:
            - in: path
              name: cart_line_id
              required: true
              schema:
                type: integer
              description: ID of the CartLine to associate with the API consumer
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
              description: CartLine not found
            500:
              description: Internal server error
        """
        user = get_user()
        cart_line = db.session.query(CartLine).filter(
            CartLine.id == cart_line_id and CartLine.created_by == user).first()
        service = db.session.query(Service).filter(Service.cart_lines.any(id=cart_line_id)).first()
        param_value = db.session.query(ParameterValue).filter(
            ParameterValue.cart_line_id == cart_line_id,
            ParameterValue.created_by == user
        ).first()


        if not cart_line:
            return Response("CartLine not found", status=400)

        try:
            consumer_username = f"cart_line_{cart_line.id}_user"
            api_key = secrets.token_hex(16)
            apisix_service = ApiSixService()

            response = apisix_service.create_consumer(
                username=consumer_username, api_key=api_key
            )

            api_key_data = response.get("value", {}).get(
                "plugins", {}).get("key-auth", {}).get("key")

            if not api_key_data:
                raise Exception("Unexpected API response format")

            if param_value:
                param_value.value = api_key_data  
            else:
                parameter = db.session.query(Parameter).filter(
                    Parameter.type == "token" and Parameter.service_id==service.id).first()
                if not parameter:
                    return Response("No valid Parameter of type 'token' found", status=400)
                param_value = ParameterValue(
                    value=api_key_data,
                    cart_line_id=cart_line.id,
                    created_by=user,
                    parameter_id=parameter.id
                )
                db.session.add(param_value)

            db.session.commit()

            return jsonify({"auth-key": api_key_data}), 200

        except Exception as e:
            _logger.error(f"Error creating API consumer: {e}", exc_info=True)
            return Response("Internal Server Error", status=500)


appbuilder.add_api(ConsumerApi)
