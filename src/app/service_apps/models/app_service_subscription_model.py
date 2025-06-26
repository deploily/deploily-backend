# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.models import Subscription


class SubscriptionAppService(Subscription):
    __tablename__ = "subscription_app_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_app_service",
    }
    type = Column(String(50), default="subscription_app_service", nullable=False)

    application_status = Column(
        Enum("processing", "deployed", "error", name="application_status"),
        default="processing",
    )
    required_restart = Column(Boolean, default=False)
    access_url = Column(String(100))
    deployment_error = Column("error", Text())

    version_id = Column(Integer, ForeignKey("version.id"))
    version = relationship("Version", back_populates="app_subscriptions")
