# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from flask import Response, jsonify, request
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.models import Cart, CartLine, Service

_logger = logging.getLogger(__name__)


class CartApi(BaseApi):
    resource_name = "cart"

    @protect()
    @jwt_required()
    @expose("/", methods=["POST"])
    def create_cart(self):
        """
        Creates a cart with the status "confirm" and adds an associated cart line.
        ---
        post:
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    service_id:
                      type: integer
                      description: ID du service à ajouter au panier
                  required:
                    - service_id
          responses:
            200:
              description: OK
            400:
              description: Bad request
            500:
              description: Internal server error
        """

        data = request.get_json()
        service_id = data.get("service_id")
        duration_month = data.get("duration_month", 1)

        if not service_id:
            return Response("The service_id field is required", status=400)

        service = db.session.query(Service).filter_by(id=service_id).first()
        if not service:
            return Response("Service not found", status=400)

        try:

            cart = Cart(status="confirm", total_amount=service.unit_price)
            db.session.add(cart)
            db.session.commit()

            if not cart.id:
                raise Exception("Cart ID not generated")

            cart_line = CartLine(
                service_id=service.id,
                amount=service.unit_price,
                duration_month=duration_month,
                start_date=datetime.now().replace(microsecond=0),
                cart_id=cart.id,
            )
            db.session.add(cart_line)

            db.session.commit()

            return jsonify({"message": "Cart and CartLine created", "cart_id": cart.id}), 200

        except Exception as e:
            db.session.rollback()
            _logger.error(f"Error creating cart: {e}")
            return Response("Internal Server Error", status=500)


appbuilder.add_api(CartApi)
