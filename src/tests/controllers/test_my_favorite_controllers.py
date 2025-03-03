# -*- coding: utf-8 -*-
import json
from datetime import timedelta
from typing import Optional
from typing import Union


import pytest
from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

my_favorite_response_data = {
    "service_id": 1,
    "created_by": 1
}

updated_my_favorite_response_data = {
    "service_id": 2,
    "created_by": {"id": 1}
}


class UserSchema(BaseModel):
    id: int
    username: Optional[str] = None


class MyFavorite(BaseModel):
    service_id: Optional[int] = None
    created_by: UserSchema


class MyFavoriteResponse(BaseModel):
    id: Optional[int] = None
    result: MyFavorite


class MyFavoriteListResponse(BaseModel):
    count: int
    result: list[MyFavorite]


def test_create_supprotticketresponse(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.my_favorites_controller import (
            MyFavoritesModelApi,
        )

        appbuilder.add_api(MyFavoritesModelApi)

        response = client.post(
            "/api/v1/myfavorites/",
            data=json.dumps(my_favorite_response_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 201
        try:
            MyFavoriteResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(
                f"ValidationError occurred on POST myfavoriteresponse : {e}")


def test_update_supportticket_response(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.my_favorites_controller import (
            MyFavoritesModelApi,
        )

        appbuilder.add_api(MyFavoritesModelApi)

        response = client.put(
            f"/api/v1/myfavorites/{1}",
            data=json.dumps(updated_my_favorite_response_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        try:
            updated_supportticketresponse = (
                MyFavoriteResponse.model_validate_json(response.text)
            )
        except ValidationError as e:
            pytest.fail(
                f"ValidationError occurred on PUT supportticketresponse : {e}")

        assert (
            updated_supportticketresponse.result.service_id
            == updated_my_favorite_response_data["service_id"]
        )


def test_get_supportticket(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.my_favorites_controller import (
            MyFavoritesModelApi,
        )

        appbuilder.add_api(MyFavoritesModelApi)

        response = client.get(
            "/api/v1/myfavorites/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        try:
            MyFavoriteListResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(
                f"ValidationError occurred on GET SupportTicketResponse : {e}")


def test_delete_supportticket(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.my_favorites_controller import (
            MyFavoritesModelApi,
        )

        appbuilder.add_api(MyFavoritesModelApi)

        response = client.delete(
            f"/api/v1/myfavorites/{2}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_authenticated_access(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.my_favorites_controller import (
            MyFavoritesModelApi,
        )

        appbuilder.add_api(MyFavoritesModelApi)

        response = client.get(
            "/api/v1/myfavorites/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_unauthenticated_access(client, app, appbuilder):
    with app.app_context():
        from app.controllers.my_favorites_controller import (
            MyFavoritesModelApi,
        )
        appbuilder.add_api(MyFavoritesModelApi)

        response = client.get(
            "/api/v1/myfavorites/",
            headers={},
        )

        assert response.status_code == 401


def test_token_expired(client, app, test_user, appbuilder):
    expired_access_token = create_access_token(
        test_user.id, expires_delta=timedelta(seconds=-1)
    )

    with app.app_context():
        from app.controllers.my_favorites_controller import (
            MyFavoritesModelApi,
        )

        appbuilder.add_api(MyFavoritesModelApi)

        response = client.get(
            "/api/v1/myfavorites/",
            headers={"Authorization": f"Bearer {expired_access_token}"},
        )

        assert response.status_code == 401
