# -*- coding: utf-8 -*-
import json
import pytest
from pydantic import BaseModel, ValidationError
from flask_jwt_extended import create_access_token
from app.models import CartLine
from app import db


class ConsumerResponse(BaseModel):
    auth_key: str


def test_create_cart_line_consumer_not_found(client, test_user, app, appbuilder):
    """Test de création d'un API consumer avec un CartLine inexistant"""
    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.consumer_controllers import ConsumerApi
        appbuilder.add_api(ConsumerApi)

        response = client.post(
            "/api/v1/consumer/cart-line/9999",
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 400
        assert response.text == "CartLine not found"


def test_create_cart_line_consumer_unauthenticated(client, app, appbuilder):
    """Test de création d'un API consumer sans authentification"""
    with app.app_context():
        from app.controllers.consumer_controllers import ConsumerApi
        appbuilder.add_api(ConsumerApi)

        response = client.post(
            "/api/v1/consumer/cart-line/1",
            content_type="application/json",
            headers={},
        )

        assert response.status_code == 401


