# # -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token
from pydantic import BaseModel, ValidationError

from app import db
from app.core.models.promo_code_models import PromoCode


class PromoCodeValidResponse(BaseModel):
    rate: float
    message: str


class PromoCodeErrorResponse(BaseModel):
    error: str


def test_valid_promo_code(client, test_user, app, appbuilder):
    token = create_access_token(test_user.id, expires_delta=False)

    with app.app_context():
        promo = PromoCode(
            code="VALID2025",
            rate=20.0,
            expiration_date=datetime.utcnow() + timedelta(days=30),  # Valid for 30 days
        )
        db.session.add(promo)
        db.session.commit()

        from app.core.controllers.promo_code_controllers import PromoCodeApi

        appbuilder.add_api(PromoCodeApi)

        response = client.get(
            "/api/v1/promo-code/?promo_code=VALID2025", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        try:
            PromoCodeValidResponse.model_validate_json(response.text)
        except ValidationError as e:
            assert False, f"ValidationError for valid promo code: {e}"


def test_invalid_promo_code(client, test_user, app, appbuilder):
    token = create_access_token(test_user.id, expires_delta=False)

    with app.app_context():

        from app.core.controllers.promo_code_controllers import PromoCodeApi

        appbuilder.add_api(PromoCodeApi)

        response = client.get(
            "/api/v1/promo-code/?promo_code=NONEXISTENT",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        try:
            PromoCodeErrorResponse.model_validate_json(response.text)
        except ValidationError as e:
            assert False, f"ValidationError for invalid promo code: {e}"


def test_expired_promo_code(client, test_user, app, appbuilder):
    token = create_access_token(test_user.id, expires_delta=False)

    with app.app_context():
        promo = PromoCode(
            code="INVALID2025",
            rate=20.0,
            expiration_date=datetime.utcnow() - timedelta(days=30),
        )
        db.session.add(promo)
        db.session.commit()

        from app.core.controllers.promo_code_controllers import PromoCodeApi

        appbuilder.add_api(PromoCodeApi)

        response = client.get(
            "/api/v1/promo-code/?promo_code=INVALID2025",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 400
        try:
            PromoCodeErrorResponse.model_validate_json(response.text)
        except ValidationError as e:
            assert False, f"ValidationError for invalid promo code: {e}"


def test_unauthenticated_access_to_promo_code(client, app, appbuilder):
    with app.app_context():
        from app.core.controllers.promo_code_controllers import PromoCodeApi

        appbuilder.add_api(PromoCodeApi)

        response = client.get("/api/v1/promo-code/")
        assert response.status_code == 401


def test_expired_token_access(client, test_user, app, appbuilder):
    token = create_access_token(test_user.id, expires_delta=timedelta(seconds=-1))

    with app.app_context():
        from app.core.controllers.promo_code_controllers import PromoCodeApi

        appbuilder.add_api(PromoCodeApi)

        response = client.get("/api/v1/promo-code/", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 401
