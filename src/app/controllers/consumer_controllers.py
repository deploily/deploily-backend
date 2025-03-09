import logging
import secrets
import uuid
from flask import Response, jsonify
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required
import os
from app import appbuilder, db
from app.models import CartLine, Parameter, ParameterValue, Service
from app.services.apisix_service import ApiSixService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class ConsumerApi(BaseApi):
    resource_name = "cart-line"

    @protect()
    @jwt_required()
    @expose("/<int:cart_line_id>/consumer", methods=["POST"])
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
        cart_line = (
            db.session.query(CartLine)
            .filter(CartLine.id == cart_line_id and CartLine.created_by == user)
            .first()
        )
        service = db.session.query(Service).filter(
            Service.cart_lines.any(id=cart_line_id)).first()
        param_value = (
            db.session.query(ParameterValue)
            .filter(ParameterValue.cart_line_id == cart_line_id, ParameterValue.created_by == user)
            .first()
        )

        if not cart_line:
            return Response("CartLine not found", status=400)

        try:
      
            api_key = uuid.uuid4().hex[:32]
            consumer_username = f"cart_line_{cart_line.id}_user"
            apisix_service = ApiSixService()
            services = (
                        db.session.query(Service)
                        .join(Service.cart_lines)  
                        .filter(CartLine.id == cart_line_id)
                        .all()
                    )

            service_labels = [service.name for service in services] if services else []

            response = apisix_service.create_consumer(
                                        username=consumer_username, api_key=api_key, labels={"services": ",".join(service_labels)}
                                    )


          

            if not api_key:
                raise Exception("Unexpected API response format")

            if param_value:
                param_value.value = api_key
            else:
                # Trouver ou créer un paramètre de type 'token' s'il n'existe pas
                parameter = (
                    db.session.query(Parameter)
                    .filter(Parameter.type == "token" and Parameter.service_id == service.id)
                    .first()
                )
                if not parameter:
                    return Response("No valid Parameter of type 'token' found", status=400)
                param_value = ParameterValue(
                    value=api_key,
                    cart_line_id=cart_line.id,
                    created_by=user,
                    parameter_id=parameter.id,
                )
                db.session.add(param_value)

            db.session.commit()

            return jsonify({"auth-key": api_key}), 200

        except Exception as e:
            _logger.error(f"Error creating API consumer: {e}", exc_info=True)
            return Response("Internal Server Error", status=500)


appbuilder.add_api(ConsumerApi)
