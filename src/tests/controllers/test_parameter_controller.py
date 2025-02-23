# -*- coding: utf-8 -*-
import json
import pytest
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel, ValidationError
from flask_jwt_extended import create_access_token

parameter_data = {
    "name": "API Key",
    "type": "token",
    "service_id": 1,  
}

updated_parameter_data = {"name": "Updated API Key"}


class Parameter(BaseModel):
    name: str
    type: str
    service_id: int


class ParameterResponse(BaseModel):
    id: Optional[int] = None
    result: Parameter


class ParameterListResponse(BaseModel):
    count: int
    result: list[Parameter]


def test_create_parameter(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.parameters_controllers import ParametersModelApi
        appbuilder.add_api(ParametersModelApi)

        response = client.post(
            "/api/v1/parameter/",
            data=json.dumps(parameter_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        try:
            ParameterResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST Parameter: {e}")


def test_update_parameter(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.parameters_controllers import ParametersModelApi
        appbuilder.add_api(ParametersModelApi)

        response = client.put(
            f"/api/v1/parameter/{1}",
            data=json.dumps(updated_parameter_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        try:
            updated_parameter = ParameterResponse.model_validate_json(
                response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on PUT Parameter: {e}")

        assert updated_parameter.result.name == updated_parameter_data["name"]


def test_get_parameters(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.parameters_controllers import ParametersModelApi
        appbuilder.add_api(ParametersModelApi)

        response = client.get(
            "/api/v1/parameter/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        try:
            ParameterListResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on GET Parameter: {e}")


def test_delete_parameter(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.parameters_controllers import ParametersModelApi
        appbuilder.add_api(ParametersModelApi)

        response = client.delete(
            f"/api/v1/parameter/{1}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_authenticated_access(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.parameters_controllers import ParametersModelApi
        appbuilder.add_api(ParametersModelApi)

        response = client.get(
            "/api/v1/parameter/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_unauthenticated_access(client, app, appbuilder):
    with app.app_context():
        from app.controllers.parameters_controllers import ParametersModelApi
        appbuilder.add_api(ParametersModelApi)

        response = client.get("/api/v1/parameter/", headers={})

        assert response.status_code == 401


def test_token_expired(client, app, test_user, appbuilder):
    expired_access_token = create_access_token(
        test_user.id, expires_delta=timedelta(seconds=-1))

    with app.app_context():
        from app.controllers.parameters_controllers import ParametersModelApi
        appbuilder.add_api(ParametersModelApi)

        response = client.get(
            "/api/v1/parameter/",
            headers={"Authorization": f"Bearer {expired_access_token}"},
        )

        assert response.status_code == 401
