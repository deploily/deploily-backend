# -*- coding: utf-8 -*-
import json
from datetime import timedelta
from typing import Optional

import pytest
from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

service_tag_data = {
    "name": "Test Service Tag",
    "color": "Green",
}

updated_service_tag_data = {"name": "Updated Service Tag"}


class ServiceTag(BaseModel):
    name: str
    color: str


class ServiceTagResponse(BaseModel):
    id: Optional[int] = None
    result: ServiceTag


class ServiceTagListResponse(BaseModel):
    count: int
    result: list[ServiceTag]


def test_create_service_tag(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.service_tag_controllers import ServiceTagModelApi

        appbuilder.add_api(ServiceTagModelApi)

        response = client.post(
            "/api/v1/service-tag/",
            data=json.dumps(service_tag_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 201
        try:
            ServiceTagResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST Service TAg : {e}")


def test_update_service_tag(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.service_tag_controllers import ServiceTagModelApi

        appbuilder.add_api(ServiceTagModelApi)

        response = client.put(
            f"/api/v1/service-tag/{1}",
            data=json.dumps(updated_service_tag_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        try:
            updated_service = ServiceTagResponse.model_validate_json(
                response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on PUT Service Tag : {e}")

        assert updated_service.result.name == updated_service_tag_data["name"]


def test_get_service_tag(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.service_tag_controllers import ServiceTagModelApi

        appbuilder.add_api(ServiceTagModelApi)

        response = client.get(
            "/api/v1/service-tag/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        try:
            ServiceTagListResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on GET Service Tag : {e}")


def test_delete_service_tag(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.service_tag_controllers import ServiceTagModelApi

        appbuilder.add_api(ServiceTagModelApi)

        response = client.delete(
            f"/api/v1/service-tag/{1}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_authenticated_access(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.service_tag_controllers import ServiceTagModelApi

        appbuilder.add_api(ServiceTagModelApi)

        response = client.get(
            "/api/v1/service-tag/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_unauthenticated_access(client, app, appbuilder):
    with app.app_context():
        from app.controllers.service_tag_controllers import ServiceTagModelApi

        appbuilder.add_api(ServiceTagModelApi)

        response = client.get(
            "/api/v1/service-tag/",
            headers={},
        )

        assert response.status_code == 401


def test_token_expired(client, app, test_user, appbuilder):
    expired_access_token = create_access_token(
        test_user.id, expires_delta=timedelta(seconds=-1))

    with app.app_context():
        from app.controllers.service_tag_controllers import ServiceTagModelApi

        appbuilder.add_api(ServiceTagModelApi)

        response = client.get(
            "/api/v1/service-tag/",
            headers={"Authorization": f"Bearer {expired_access_token}"},
        )

        assert response.status_code == 401
