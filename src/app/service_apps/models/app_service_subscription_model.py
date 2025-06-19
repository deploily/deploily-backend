# -*- coding: utf-8 -*-

from sqlalchemy import Column, Enum, ForeignKey, Integer, String

from app.core.models import Subscription


class SubscriptionAppService(Subscription):
    __tablename__ = "subscription_app_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_app_service",
    }
    type = Column(String(50), default="subscription_app_service", nullable=False)
    url_segment = Column(String, nullable=False)

    application_status = Column(
        Enum("processing", "deployed", name="application_status"),
        default="processing",
    )
