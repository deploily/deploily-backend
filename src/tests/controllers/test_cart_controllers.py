# -*- coding: utf-8 -*-
import json
import pytest
from datetime import datetime
from pydantic import BaseModel, ValidationError
from flask_jwt_extended import create_access_token
from app.models import Service, Cart, CartLine
from app import db

cart_data = {"service_id": 1, "duration_month": 3}


class CartResponse(BaseModel):
    message: str


def test_create_cart(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True
    )

    with app.app_context():
        from app.controllers.cart_controllers import CartApi
        appbuilder.add_api(CartApi)

        service = Service(id=1, name="Test Service", documentation_url="This is a test service",
                          service_url="https://example.com/service", description="This is a test service", unit_price=100.0)
        db.session.add(service)
        db.session.commit()

        response = client.post(
            "/api/v1/cart/",
            data=json.dumps(cart_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        try:
            CartResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST Cart: {e}")


def test_create_cart_missing_service_id(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True
    )

    with app.app_context():
        from app.controllers.cart_controllers import CartApi
        appbuilder.add_api(CartApi)

        response = client.post(
            "/api/v1/cart/",
            data=json.dumps({}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.text == "The service_id field is required"


def test_create_cart_with_non_existent_service(client, test_user, app, appbuilder):
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True
    )

    with app.app_context():
        from app.controllers.cart_controllers import CartApi
        appbuilder.add_api(CartApi)

        response = client.post(
            "/api/v1/cart/",
            data=json.dumps({"service_id": 9999}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.text == "Service not found"

  
        db.session.rollback()


def test_create_cart_unauthenticated(client, app, appbuilder):
    with app.app_context():
        from app.controllers.cart_controllers import CartApi
        appbuilder.add_api(CartApi)

        response = client.post(
            "/api/v1/cart/",
            data=json.dumps(cart_data),
            content_type="application/json",
            headers={},
        )

        assert response.status_code == 401
