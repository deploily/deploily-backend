import logging
import os
import random
import string
from datetime import datetime

from dateutil.relativedelta import relativedelta  # Requires python-dateutil
from flask import jsonify, request
from flask_appbuilder.api import BaseApi, expose

from app import appbuilder, db
from app.core.models.promo_code_models import PromoCode
from app.promo_code.models.api_tokens_model import ApiToken

_logger = logging.getLogger(__name__)


class ClientPromoCodeApi(BaseApi):
    resource_name = "client"

    @expose("/promo-code", methods=["POST"])
    def get_promo_code(self):
        """
        Retrieves a promo code based on the token provided in the Authorization header.
        ---
        post:
            summary: Retrieve promo code using API token
            description: |
                Checks the Authorization header for a valid token.
                If valid, returns the associated promo code.
            security:
                - ApiKeyAuth: []
            parameters:
              - name: X-API-KEY
                in: header
                required: true
                schema:
                    type: string
                description: API key to access this endpoint

            responses:
                200:
                    description: Promo code successfully retrieved
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    promo_code:
                                        type: string
                401:
                    description: Unauthorized - missing or invalid token
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
                                        example: unauthorized
                                    message:
                                        type: string
                                        example: Invalid token
                500:
                    description: Internal server error
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
        """

        try:
            token = request.headers.get("X-API-KEY")

            if not token:
                return (
                    jsonify(
                        {"error": "unauthorized", "message": "Missing token in X-API-KEY header"}
                    ),
                    401,
                )

            api_token = db.session.query(ApiToken).filter_by(token=token).first()

            if not api_token:
                return jsonify({"error": "unauthorized", "message": "Invalid token"}), 401

            # Generate promo code
            random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            generated_code = f"{api_token.token_prefix}-{random_part}"

            # Get duration from env or default to 3 months
            try:
                months = int(os.environ.get("PROMO_CODE_DURATION_MONTHS", 3))
            except ValueError:
                _logger.warning("Invalid PROMO_CODE_DURATION_MONTHS env value. Falling back to 3.")
                months = 3

            expiration_date = datetime.now() + relativedelta(months=months)

            # Get rate from env or default to 100
            try:
                rate = int(os.environ.get("PROMO_CODE_RATE", 100))
            except ValueError:
                _logger.warning("Invalid PROMO_CODE_RATE env value. Falling back to 100.")
                rate = 100

            promo_code = PromoCode(
                code=generated_code,
                expiration_date=expiration_date.replace(microsecond=0),
                rate=rate,
            )

            db.session.add(promo_code)
            db.session.commit()

            return (
                jsonify(
                    {
                        "promo_code": generated_code,
                        "expiration_date": expiration_date.replace(microsecond=0).isoformat(),
                    }
                ),
                200,
            )

        except Exception as e:
            _logger.exception("Failed to generate promo code")
            return (
                jsonify(
                    {
                        "error": "server_error",
                        "message": "An unexpected error occurred",
                        "details": str(e),
                    }
                ),
                500,
            )


appbuilder.add_api(ClientPromoCodeApi)
