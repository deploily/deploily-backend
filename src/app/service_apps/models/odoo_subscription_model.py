# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String

from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)


class OdooSubscriptionAppService(SubscriptionAppService):
    __tablename__ = "odoo_subscription_app_service"
    id = Column(Integer, ForeignKey("subscription_app_service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "odoo",
    }
    odoo_password = Column(String, nullable=True)
