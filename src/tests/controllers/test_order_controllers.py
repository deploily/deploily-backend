# # -*- coding: utf-8 -*-

# import json
# from typing import Optional, Union
# from datetime import timedelta
# from flask_jwt_extended import create_access_token
# from pydantic import ConfigDict, ValidationError, BaseModel
# import pytest
# import logging

# logging.basicConfig(level=logging.DEBUG) 

# cart_data = {
#     "status": "draft",
#     "user": 1,
#     "total_amount": 85.32
# }

# updated_data = {"total_amount": 85.32}

# class UserResponse(BaseModel):
#     id: int
#     username: Optional[str] = None
#     email: Optional[str] = None

# class Cart(BaseModel):
#     model_config = ConfigDict(strict=True)
#     status: Optional[str] = None
#     total_amount: Optional[float] = None  
#     user: Union[int, UserResponse]
    
# class CartListResponse(BaseModel):
#     count: int
#     result: list[Cart]

# class CartResponse(BaseModel):
#     model_config = ConfigDict(strict=True)
#     id: Optional[int] = None
#     result: Cart

# def test_create_cart(client, test_user, app, appbuilder):
#     """Test POST cart"""
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True
#     )

#     cart_data["user"] = test_user.id  

#     print("Cart Data Sent:", json.dumps(cart_data, indent=2)) 

#     with app.app_context():
#         from app.controllers.cart_controllers import CartModelApi

#         appbuilder.add_api(CartModelApi)

#         response = client.post(
#             "/api/v1/cart/",
#             json=cart_data,
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

#         assert response.status_code == 201, f"Unexpected status code: {response.status_code}"

#         try:
#             CartResponse.model_validate_json(response.text)
#         except ValidationError as e:
#             pytest.fail(f"ValidationError occurred on POST Cart: {e}")

# def test_update_cart(client, test_user, app, appbuilder):
#     """Test PUT cart"""
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True
#     )

#     cart_id = 1  

#     with app.app_context():
#         from app.controllers.cart_controllers import CartModelApi

#         appbuilder.add_api(CartModelApi)

#         response = client.put(
#             f"/api/v1/cart/{cart_id}",
#             json=updated_data,
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

#         print("Response Status Code:", response.status_code)
#         print("Response Body:", response.text)

#         assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

#         try:
#             updated_cart = CartResponse.model_validate_json(response.text)
#         except ValidationError as e:
#             pytest.fail(f"ValidationError occurred on PUT Cart: {e}")

#         assert updated_cart.result.total_amount == updated_data["total_amount"]

# def test_get_cart(client, test_user, app, appbuilder):
#     """Test GET cart"""
#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True
#     )
#     with app.app_context():
#         from app.controllers.cart_controllers import CartModelApi

#         appbuilder.add_api(CartModelApi)

#         response = client.get(
#             "/api/v1/cart/",
#             headers={
#                 "accept": "application/json",
#                 "Authorization": f"Bearer {access_token}",
#             },
#         )

#         assert response.status_code == 200
#         try:
#             CartListResponse.model_validate_json(response.text)
#         except ValidationError as e:
#             pytest.fail(f"ValidationError occurred on GET Cart: {e}")




# def test_delete_cart(client, test_user, app, appbuilder):
#     """Test DELETE cart"""

#     access_token = create_access_token(
#         test_user.id, expires_delta=False, fresh=True
#     )
#     with app.app_context():
#         from app.controllers.cart_controllers import CartModelApi

#         appbuilder.add_api(CartModelApi)

#         response = client.delete(
#             f"/api/v1/cart/{1}",
#             content_type="application/json",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

#         assert response.status_code == 200

# def test_authenticated_access(client, test_user, app, appbuilder):
#     """Test access with valid authentication token"""
   
#     access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)
    
#     with app.app_context():
#         from app.controllers.cart_controllers import CartModelApi
#         appbuilder.add_api(CartModelApi)

#         response = client.get(
#             "/api/v1/cart/",
#             headers={"Authorization": f"Bearer {access_token}"},
#         )

       
#         assert response.status_code == 200

# def test_unauthenticated_access(client, app, appbuilder):
#     """Test access without authentication token"""
#     with app.app_context():
#         from app.controllers.cart_controllers import CartModelApi
#         appbuilder.add_api(CartModelApi)

     
#         response = client.get(
#             "/api/v1/cart/",
#             headers={}, 
#         )

#         assert response.status_code == 401

# def test_token_expired(client, app, test_user,appbuilder):
#     """Test access with expired token"""
#     expired_access_token = create_access_token(test_user.id, expires_delta=timedelta(seconds=-1))
#     with app.app_context():
#         from app.controllers.cart_controllers import CartModelApi
#         appbuilder.add_api(CartModelApi)
#         response = client.get(
#             "/api/v1/cart/",
#             headers={"Authorization": f"Bearer {expired_access_token}"},
#         )
#         assert response.status_code == 401





