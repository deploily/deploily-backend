import logging
import random
import string

from flask import request
from flask_appbuilder.api import BaseApi, expose

from app import appbuilder, db
from app.promo_code.models.api_tokens_model import ApiToken

_logger = logging.getLogger(__name__)


class ClientPromoCodeApi(BaseApi):
    resource_name = "client"

    @expose("/promo-code", methods=["GET"])
    def get_promo_code(self):
        """
        Retrieves a promo code based on the token provided in the Authorization header.
        ---
        get:
            summary: Retrieve promo code using API token
            description: |
                Checks the Authorization header for a valid token.
                If valid, returns the associated promo code.

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
            token = request.headers.get("Authorization")
            if not token:
                message = "Missing token in Authorization header"
                return message

            if token.startswith("Bearer "):
                token = token[7:]

            api_token = db.session.query(ApiToken).all()
            for token_obj in api_token:
                if token_obj.token == token:
                    print(
                        f"#################################Valid token found: {len(token_obj.token)}"
                    )
                    print(f"#################################Valid token found: {len(token)}")
                    token_exists = True
                    break

            if not token_exists:

                message = "Invalid token"
                return message

            generated_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

            result = {"promo_code": generated_code}
            return result
        except Exception as e:
            return self.response_500(message="Server error", error=str(e))


appbuilder.add_api(ClientPromoCodeApi)
