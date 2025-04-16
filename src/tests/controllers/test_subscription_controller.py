# -*- coding: utf-8 -*-

import json

from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

"""
"form_url": "string",
  "order_id": "string",
  "subscription": {
    "duration_month": 0,
    "id": 0,
    "name": "string",
    "price": 0,
    "promo_code_id": 0,
    "service_plan_id": 0,
    "start_date": "2025-04-16T14:08:09.816Z",
    "status": "string",
    "total_amount": 0
  }
"""
balance_sufficient_request = {
    "duration": 5,
    "profile_id": 1,
    "service_plan_selected_id": 1,
}
balance_non_sufficient_request = {
    "form_url": "",
    "order_id": "",
    "subscription": {
        "duration_month": 5,
        "id": 32,
        "name": "Level 1 BASIC",
        "price": 600,
        "promo_code_id": None,
        "service_plan_id": 1,
        "status": "active",
        "total_amount": 600,
    },
}


class Subscription(BaseModel):
    duration_month: int
    id: int
    name: str
    price: int
    promo_code_id: int
    service_plan_id: int
    start_date: int
    status: int
    total_amount: int


class SubscriptionRequest(BaseModel):
    duration: int
    payment_method: str
    profile_id: int
    promo_code: str
    service_plan_selected_id: int
    total_amount: int


class SubscribeResponse(BaseModel):
    form_url: str
    order_id: str
    subscription: Subscription


def test_create_subscribe_with_suffecient_balance(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app.controllers.subscribe_service_plan_controllers import SubscriptionApi

        appbuilder.add_api(SubscriptionApi)
        response = client.post(
            "/api/v1/service-subscription/subscribe",
            data=json.dumps(balance_sufficient_request),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        try:
            SubscribeResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST myfavoriteresponse : {e}")
