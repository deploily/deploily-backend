# -*- coding: utf-8 -*-

import json
from typing import Optional
from flask_jwt_extended import create_access_token
from pydantic import ConfigDict, ValidationError
from pydantic import BaseModel
import pytest

cart_data = {"name": "Test Cart", "status": "draft"}
updated_data = {"name": "Updated Cart"}
cart_data_response = {"id": "1", "result": cart_data}


class Cart(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str
    status: Optional[str] = None
    service: list

class CartListResponse(BaseModel):
    count: int
    result: list[Cart]

class CartReponse(BaseModel):
    model_config = ConfigDict(strict=True)
    id: Optional[int] = None
    result: Cart


def test_create_cart(client, test_user, app, appbuilder):
    """Test POST cart"""

    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True
    )
    with app.app_context():
        from app.controllers.cart_controllers import CartModelApi

        appbuilder.add_api(CartModelApi)

        response = client.post(
            "/api/v1/cart/",
            data=json.dumps(cart_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 201
        try:
            # Auto validation & deserialization by pyndatic
            CartReponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST Cart : {e}")


def test_update_cart(client, test_user, app, appbuilder):
    """Test PUT cart"""

    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True
    )
    with app.app_context():
        from app.controllers.cart_controllers import CartModelApi

        appbuilder.add_api(CartModelApi)

        response = client.put(
            f"/api/v1/cart/{1}",
            data=json.dumps(updated_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        try:
            # Auto validation & deserialization by pyndatic
            updated_cart = CartReponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on PUT Cart : {e}")

      
        assert updated_cart.result.name == updated_data["name"]
       

def test_get_cart(client, test_user, app, appbuilder):
    """Test GET cart"""

    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True
    )
    with app.app_context():
        from app.controllers.cart_controllers import CartModelApi

        appbuilder.add_api(CartModelApi)

        response = client.get(
            "/api/v1/cart/",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )
       

        assert response.status_code == 200
        try:
            # Auto validation & deserialization by pyndatic
            CartListResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST Cart : {e}")



def test_delete_cart(client, test_user, app, appbuilder):
    """Test DELETE cart"""

    access_token = create_access_token(
        test_user.id, expires_delta=False, fresh=True
    )
    with app.app_context():
        from app.controllers.cart_controllers import CartModelApi

        appbuilder.add_api(CartModelApi)

        response = client.delete(
            f"/api/v1/cart/{1}",
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
