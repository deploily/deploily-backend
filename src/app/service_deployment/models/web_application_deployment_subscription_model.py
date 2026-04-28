# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.service_deployment.models.deployment_service_subscription_model import (
    SubscriptionDeploymentService,
)


class WebApplicationSubscriptionDeploymentService(SubscriptionDeploymentService):
    __tablename__ = "web_application_subscription_deployment_service"
    id = Column(Integer, ForeignKey("subscription_deployment_service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "web_application_deployment",
    }
    description = Column(Text, nullable=True)
