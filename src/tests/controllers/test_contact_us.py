# -*- coding: utf-8 -*-
import json
from datetime import timedelta
from typing import List

import pytest
from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

contact_us_data = {
    "id": 1,
    "name": "contact_us_test",
    "email": "aichouchec40@gmail.com",
    "message": "Hello, I would like to know more about your services.",
}
contact_us_update_data = {
    "id": 1,
    "name": "contact_us_test_updated",
    "email": "aichouchec40@gmail.com",
    "message": "Hello, I would like to know more about your services....",
}


class ContactUsSchema(BaseModel):
    id: int
    name: str
    email: str
    message: str


class ContactUsResponse(BaseModel):
    id: int
    result: ContactUsSchema


class ContactUsListResponse(BaseModel):
    count: int
    result: List[ContactUsSchema]


def test_create_contact_us(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.contact_us_controllers import ContactUSModelApi

        appbuilder.add_api(ContactUSModelApi)

        response = client.post(
            "/api/v1/contact-us/",
            data=json.dumps(contact_us_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
        try:
            ContactUsResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"Validation error on POST contact-us: {e}")


def test_update_contact_us(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.contact_us_controllers import ContactUSModelApi

        appbuilder.add_api(ContactUSModelApi)

        response_update = client.put(
            f"/api/v1/contact-us/{1}",
            data=json.dumps(contact_us_update_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response_update.status_code == 200
        updated_response = response_update.get_json()
        assert updated_response["result"]["name"] == contact_us_update_data["name"]
        assert updated_response["result"]["email"] == contact_us_update_data["email"]
        assert updated_response["result"]["message"] == contact_us_update_data["message"]


def test_get_contact_us(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.contact_us_controllers import ContactUSModelApi

        appbuilder.add_api(ContactUSModelApi)

        response = client.get(
            "/api/v1/contact-us/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        try:
            ContactUsListResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"Validation error on GET contact-us: {e}")


def test_delete_contact_us(client, test_user, app, appbuilder):

    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.core.controllers.contact_us_controllers import ContactUSModelApi

        appbuilder.add_api(ContactUSModelApi)

        response = client.delete(
            f"/api/v1/contact-us/{1}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200


def test_unauthenticated_access_contact_us(client, app, appbuilder):
    with app.app_context():
        from app.core.controllers.contact_us_controllers import ContactUSModelApi

        appbuilder.add_api(ContactUSModelApi)

        response = client.get("/api/v1/contact-us/")
        assert response.status_code == 401


def test_token_expired_contact_us(client, app, test_user, appbuilder):
    expired_token = create_access_token(test_user.id, expires_delta=timedelta(seconds=-1))

    with app.app_context():
        from app.core.controllers.contact_us_controllers import ContactUSModelApi

        appbuilder.add_api(ContactUSModelApi)

        response = client.get(
            "/api/v1/contact-us/",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401
