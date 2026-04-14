# -*- coding: utf-8 -*-

from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import current_user

from app import appbuilder


class UserModelApi(BaseApi):
    resource_name = "user"  # good practice to define this

    @expose("/me", methods=["GET"])
    @protect()
    def get_me(self):
        """
        Get the current authenticated user's profile.
        ---
        get:
          description: Retrieve the current user's profile information.
          responses:
            200:
              description: Successfully retrieved user profile
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      id:
                        type: integer
                      username:
                        type: string
                      email:
                        type: string
                      first_name:
                        type: string
                      last_name:
                        type: string
            401:
              description: Unauthorized (user not authenticated)
            500:
              description: Internal server error
        """
        if not current_user or not current_user.is_authenticated:
            return self.response_401()

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


# Register the API with AppBuilder
appbuilder.add_api(UserModelApi)
