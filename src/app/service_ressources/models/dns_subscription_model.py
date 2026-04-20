# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer

from app.service_ressources.models.subscription_ressource_service_model import (
    SubscriptionRessourceService,
)


class DnsSubscriptionService(SubscriptionRessourceService):
    __tablename__ = "dns_subscription_ressource_service"
    id = Column(Integer, ForeignKey("subscription_ressource_service.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "dns",
    }
