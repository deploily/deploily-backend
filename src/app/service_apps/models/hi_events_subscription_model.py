# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String

from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)


class HiEventSubscriptionAppService(SubscriptionAppService):
    __tablename__ = "event_subscription_app_service"
    id = Column(Integer, ForeignKey("subscription_app_service.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "event",
    }
    event_url = Column(String, nullable=True)  # Base URL of the Event app
    event_domain = Column(String, nullable=True)
