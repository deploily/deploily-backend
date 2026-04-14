# -*- coding: utf-8 -*-
import pytest
from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError


class UserProfile(BaseModel):
    username: str
    email: str


class UserProfileResponse(BaseModel):
    result: UserProfile


def test_get_current_user_profile(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False)

    with app.app_context():
        from app.core.controllers.user_profile_controllers import UserModelApi

        appbuilder.add_api(UserModelApi)

        response = client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

        try:
            UserProfileResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"Validation error on user profile response: {e}")
