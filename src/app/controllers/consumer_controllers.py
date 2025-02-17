# -*- coding: utf-8 -*-

import logging
import secrets
from datetime import datetime
from flask import request, jsonify, Response
from flask_jwt_extended import jwt_required
from flask_appbuilder.api import BaseApi, expose, protect
from app import db, appbuilder
from app.utils.utils import get_user
from app.models import CartLine
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
        cart_line = db.session.query(CartLine).filter(CartLine.id == cart_line_id and CartLine.created_by == user).first()

        
        if not cart_line:
            return Response("CartLine not found", status=400)

        try:
            consumer_username = f"cart_line_{cart_line.id}_user"
            api_key = secrets.token_hex(16)
            apisix_service = ApiSixService()

            response = apisix_service.create_consumer(
                username=consumer_username, api_key=api_key
            )
            
            api_key_data = response.get("value", {}).get("plugins", {}).get("key-auth", {}).get("key")
            
            if not api_key_data:
                raise Exception("Unexpected API response format")

            return jsonify({"auth-key": api_key_data}), 200

        except Exception as e:
            _logger.error(f"Error creating API consumer: {e}", exc_info=True)
            return Response("Internal Server Error", status=500)


appbuilder.add_api(ConsumerApi)

