# -*- coding: utf-8 -*-
import json
from datetime import timedelta
from typing import Optional

import pytest
from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

service_data = {
    "id": 198,
    "name": "Test Service",
    "description": "This is a test service",
    "documentation_url": "https://example.com/docs",
    "unit_price": 99.99,
}


class Service(BaseModel):
    name: str
    description: str
    documentation_url: str
    unit_price: Optional[float] = None
    image_service: Optional[str] = None
    parameters: Optional[list] = []


class ServiceResponse(BaseModel):
    id: Optional[int] = None
    result: Service


class ServiceListResponse(BaseModel):
    count: int
    result: list[Service]


def test_create_service(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.service_controllers import ServiceModelApi

        appbuilder.add_api(ServiceModelApi)

        response = client.post(
            "/api/v1/service/",
            data=json.dumps(service_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 201
        try:
            ServiceResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST Service : {e}")


def test_get_service(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.service_controllers import ServiceModelApi

        appbuilder.add_api(ServiceModelApi)

        response = client.get(
            "/api/v1/service/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        print(response.get_json())
        assert response.status_code == 200
        try:
            ServiceListResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on GET Service : {e}")


def test_delete_service(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.service_controllers import ServiceModelApi

        appbuilder.add_api(ServiceModelApi)

        response = client.delete(
            f"/api/v1/service/{198}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_authenticated_access(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.service_controllers import ServiceModelApi

        appbuilder.add_api(ServiceModelApi)

        response = client.get(
            "/api/v1/service/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_unauthenticated_access(client, app, appbuilder):
    with app.app_context():
        from app.core.controllers.service_controllers import ServiceModelApi

        appbuilder.add_api(ServiceModelApi)

        response = client.get(
            "/api/v1/service/",
            headers={},
        )

        assert response.status_code == 401


def test_token_expired(client, app, test_user, appbuilder):
    expired_access_token = create_access_token(test_user.id, expires_delta=timedelta(seconds=-1))

    with app.app_context():
        from app.core.controllers.service_controllers import ServiceModelApi

        appbuilder.add_api(ServiceModelApi)

        response = client.get(
            "/api/v1/service/",
            headers={"Authorization": f"Bearer {expired_access_token}"},
        )

        assert response.status_code == 401
