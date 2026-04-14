# -*- coding: utf-8 -*-

import json
from datetime import datetime
from typing import Optional, Union

import pytest
from flask_appbuilder.security.sqla.models import User
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
    "captcha_token": "6Ldb_i8rAAAAAKHLinX4bNEs8M_kofYlLtDpYuRE",
    "duration": 1,
    "payment_method": "string",
    "profile_id": 1,
    "service_plan_selected_id": 1,
    # "total_amount": 0,
    "start_date": "2025-06-11 14:52:26",
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
    price: float
    promo_code_id: Optional[int]
    service_plan_id: int
    start_date: Union[str, datetime]
    status: str
    total_amount: float


class SubscriptionRequest(BaseModel):
    duration: int
    payment_method: str
    profile_id: int
    promo_code_id: Optional[int]
    service_plan_selected_id: int
    total_amount: int
    captcha_token: str


class SubscribeResponse(BaseModel):
    form_url: str
    order_id: str
    subscription: Subscription


def test_create_subscribe_with_suffecient_balance(client, test_user, app, appbuilder):
    access_token = create_access_token(test_user.id, expires_delta=False, fresh=True)

    with app.app_context():
        from app import db
        from app.core.models.payment_profile_models import PaymentProfile

        user = db.session.get(User, test_user.id)
        payment_profile = PaymentProfile(
            created_by=user,
            name="Test Profile",
            last_name="Test Last",
            profile_type="default",
            phone="0600000000",
            is_company=False,
            address="123 rue test",
            city="Testville",
            wilaya="Alger",
            country="Algeria",
            postal_code="16000",
            changed_by_fk=1,
        )
        db.session.add(payment_profile)
        db.session.commit()

        from app.core.models.plan_models import Plan
        from app.core.models.service_plan_models import ServicePlan

        plan = Plan(
            id=1,
            name="Test Plan",
            description="Plan de test",
        )
        db.session.add(plan)
        db.session.commit()
        print("Plan created:", plan)
        print("plan_id:", plan.id)

        service_plan = ServicePlan(
            id=1,
            price=100,
            plan_id=plan.id,
        )
        db.session.add(service_plan)
        db.session.commit()
        print("Service Plan created:", service_plan)
        print("Service Plan created:", service_plan.id)

        from app.service_api.controllers.subscribe_api_service_plan_controllers import (
            SubscriptionApi,
        )

        appbuilder.add_api(SubscriptionApi)

        response = client.post(
            "/api/v1/api-service-subscription/subscribe",
            data=json.dumps(balance_sufficient_request),
            content_type="application/json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        print("Response status code:", response.status_code)
        print("Response text:", response.text)

        assert response.status_code == 200

        try:
            SubscribeResponse.model_validate_json(response.text)
        except ValidationError as e:
            pytest.fail(f"ValidationError occurred on POST response: {e}")
