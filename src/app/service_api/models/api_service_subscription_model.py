# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer

from app.core.models import Subscription


class ApiServiceSubscription(Subscription):
    __tablename__ = "subscription_api_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_api_service",
    }
