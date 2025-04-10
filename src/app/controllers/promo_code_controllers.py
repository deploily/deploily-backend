# -*- coding: utf-8 -*-

import logging

from flask import jsonify, request
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.models.promo_code_models import PromoCode

_logger = logging.getLogger(__name__)


class PromoCodeApi(BaseApi):
    resource_name = "promo-code"

    @protect()
    @jwt_required()
    @expose("/", methods=["GET"])
    def check_promo_code(self):
        """
        Checks if a promo code is valid and returns its discount rate.
        ---
        get:
          description: Checks if a promo code is valid and returns its discount rate.
          parameters:
            - name: promo_code
              in: query
              required: true
              schema:
                type: string
                example: "SUMMER2024"
              description: Promo code to check
          responses:
            200:
              description: Valid promo code
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      rate:
                        type: number
                        format: float
                        description: Discount rate applied
                      message:
                        type: string
                        description: Success message
            400:
              description: Promo code required or expired
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      error:
                        type: string
                        description: Error message
            404:
              description: Invalid promo code
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      error:
                        type: string
                        description: Error message
        """
        promo_code = request.args.get("promo_code")

        if not promo_code:
            return jsonify({"error": "Promo code required"}), 400

        promo = db.session.query(PromoCode).filter_by(code=promo_code).first()

        if not promo:
            return jsonify({"error": "Invalid promo code"}), 404

        if not promo.is_valid:
            return jsonify({"error": "Expired promo code"}), 400

        return jsonify({"rate": promo.rate, "message": "Promo code successfully applied !"}), 200


appbuilder.add_api(PromoCodeApi)
