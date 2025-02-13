# # -*- coding: utf-8 -*-

# import json
# import pytest
# from typing import Optional
# from datetime import timedelta, datetime
# from pydantic import BaseModel, ValidationError
# from flask_jwt_extended import create_access_token


# cart_line_data = {
#     "amount": 150.0,
#     "duration_month": 12,
#     "service_id": 1,
#     "cart_id": 1,
# }

# updated_cart_line_data = {"amount": 200.0}


# class CartLine(BaseModel):
#     amount: float
#     duration_month: Optional[int] = None
#     service_id: int
#     cart_id: int
#     start_date: Optional[datetime] = None


# class CartLineResponse(BaseModel):
#     id: Optional[int] = None
#     result: CartLine


# class CartLineListResponse(BaseModel):
#     count: int
#     result: list[CartLine]


# def test_create_cart_line(client, test_user, app, appbuilder):
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True)

#     with app.app_context():
#         from app.controllers.cart_line_controllers import CartLineModelApi
#         appbuilder.add_api(CartLineModelApi)

#         response = client.post(
#             "/api/v1/cartline/",
#             data=json.dumps(cart_line_data),
#             content_type="application/json",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

#         assert response.status_code == 201
#         try:
#             CartLineResponse.model_validate_json(response.text)
#         except ValidationError as e:
#             pytest.fail(f"ValidationError occurred on POST CartLine: {e}")


# def test_update_cart_line(client, test_user, app, appbuilder):
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True)

#     with app.app_context():
#         from app.controllers.cart_line_controllers import CartLineModelApi
#         appbuilder.add_api(CartLineModelApi)

#         response = client.put(
#             f"/api/v1/cartline/{1}",
#             data=json.dumps(updated_cart_line_data),
#             content_type="application/json",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

#         assert response.status_code == 200
#         try:
#             updated_cart_line = CartLineResponse.model_validate_json(
#                 response.text)
#         except ValidationError as e:
#             pytest.fail(f"ValidationError occurred on PUT CartLine: {e}")

#         assert updated_cart_line.result.amount == updated_cart_line_data["amount"]


# def test_get_cart_line(client, test_user, app, appbuilder):
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True)

#     with app.app_context():
#         from app.controllers.cart_line_controllers import CartLineModelApi
#         appbuilder.add_api(CartLineModelApi)

#         response = client.get(
#             "/api/v1/cartline/",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )
#         assert response.status_code == 200
#         try:
#             CartLineListResponse.model_validate_json(response.text)
#         except ValidationError as e:
#             pytest.fail(f"ValidationError occurred on GET CartLine: {e}")


# def test_delete_cart_line(client, test_user, app, appbuilder):
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True)

#     with app.app_context():
#         from app.controllers.cart_line_controllers import CartLineModelApi
#         appbuilder.add_api(CartLineModelApi)

#         response = client.delete(
#             f"/api/v1/cartline/{1}",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

#         assert response.status_code == 200


# def test_authenticated_access(client, test_user, app, appbuilder):
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True)

#     with app.app_context():
#         from app.controllers.cart_line_controllers import CartLineModelApi
#         appbuilder.add_api(CartLineModelApi)

#         response = client.get(
#             "/api/v1/cartline/",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

#         assert response.status_code == 200


# def test_unauthenticated_access(client, app, appbuilder):
#     with app.app_context():
#         from app.controllers.cart_line_controllers import CartLineModelApi
#         appbuilder.add_api(CartLineModelApi)

#         response = client.get(
#             "/api/v1/cartline/",
#             headers={},
#         )

#         assert response.status_code == 401


# def test_token_expired(client, app, test_user, appbuilder):
#     expired_access_token = create_access_token(
#         test_user.id, expires_delta=timedelta(seconds=-1))

#     with app.app_context():
#         from app.controllers.cart_line_controllers import CartLineModelApi
#         appbuilder.add_api(CartLineModelApi)

#         response = client.get(
#             "/api/v1/cartline/",
#             headers={"Authorization": f"Bearer {expired_access_token}"},
#         )

#         assert response.status_code == 401
