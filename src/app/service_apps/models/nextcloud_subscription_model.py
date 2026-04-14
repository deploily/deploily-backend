# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String

from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)


class NextCloudSubscriptionAppService(SubscriptionAppService):
    __tablename__ = "nextcloud_subscription_app_service"
    id = Column(Integer, ForeignKey("subscription_app_service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "nextcloud",
    }

    nextcloud_url = Column(String, nullable=True)
    nextcloud_domain = Column(String, nullable=True)
