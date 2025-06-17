# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.models import Subscription


class SubscriptionAppService(Subscription):
    __tablename__ = "subscription_app_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_app_service",
    }
    access_url = Column(Text, nullable=True)
    secret_key = Column(Text, nullable=True)
