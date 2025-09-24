# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.models import Subscription


class SubscriptionDeploymentService(Subscription):
    __tablename__ = "subscription_deployment_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_deployment_service",
    }
    type = Column(String(50), default="subscription_deployment_service", nullable=False)

    deployment_status = Column(
        Enum("processing", "deployed", "error", name="deployment_status"),
        default="processing",
    )
    required_restart = Column(Boolean, default=False)
    access_url = Column(String(100))
    deployment_error = Column("error", Text())

    custom_paramters = relationship(
        "CustomParameter",
        back_populates="deployment_subscription",
        overlaps="deployment_subscription",
    )
