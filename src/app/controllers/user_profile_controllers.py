# -*- coding: utf-8 -*-


# from flask_appbuilder import current_user
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import current_user

from app import appbuilder


class UserModelApi(BaseApi):
    @expose("/me", methods=["GET"])
    @protect()
    def get_me(self):
        """Checks the status of a payment using the order_id provided by the frontend.
        ---
        get:
            responses:
                200:
                    description: Payment status successfully retrieved
                    content:
                        application/json:
                            schema:
                                type: object

                400:
                    description: Invalid request (missing or invalid parameters)
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    error:
                                        type: string
                                    message:
                                        type: string
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
        """Returns the current user's profile"""
        user = current_user
        return self.response(
            200,
            result={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        )


appbuilder.add_api(UserModelApi)
