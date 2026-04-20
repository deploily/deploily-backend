# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.models import Subscription


class SubscriptionRessourceService(Subscription):
    __tablename__ = "subscription_ressource_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_ressource_service",
    }
    type = Column(String(50), default="subscription_ressource_service", nullable=False)
