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
    internal_note = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "is_expired": self.is_expired,
            # "short_description": self.short_description,
            # "price_period": self.price_period,
            "name": self.name,
            # "image_service": self.image_service,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "total_amount": self.total_amount,
            "price": self.price,
            # "is_in_favorite": self.is_in_favorite,
            "deployment_status": self.deployment_status,
            "payment_status": self.payment_status,
            "duration_month": self.duration_month,
            "status": self.status,
            "service_plan_id": self.service_plan.id if self.service_plan else None,
            "service_plan": {
                "id": self.service_plan.id,
                "price": self.service_plan.price,
                "subscription_category": self.service_plan.subscription_category,
            },
            "promo_code_id": self.promo_code.id if self.promo_code else None,
            "promo_code_name": self.promo_code.code if self.promo_code else None,
            "api_key": self.api_key,
            "is_encrypted": self.is_encrypted,
            "profile_id": self.profile.id if self.profile else None,
            "profile_name": (self.profile.name if hasattr(self.profile, "name") else None),
            "is_upgrade": self.is_upgrade,
            "is_renew": self.is_renew,
            "is_expired": self.is_expired,
            "service_details": {
                "id": self.service_details.get("id"),
                "name": self.service_details.get("name"),
                "description": self.service_details.get("description"),
                "documentation_url": self.service_details.get("documentation_url"),
                "api_playground_url": self.service_details.get("api_playground_url"),
                "unit_price": self.service_details.get("unit_price"),
                "price_period": self.service_details.get("price_period"),
                "service_url": self.service_details.get("service_url"),
                "image_service": self.service_details.get("image_service"),
                "short_description": self.service_details.get("short_description"),
                "specifications": self.service_details.get("specifications"),
                "curl_command": self.service_details.get("curl_command"),
                "api_key": self.service_details.get("api_key"),
                "is_subscribed": self.service_details.get("is_subscribed"),
                "service_slug": self.service_details.get("service_slug"),
                "monitoring": self.service_details.get("monitoring"),
                "ssh_access": self.service_details.get("ssh_access"),
                "type": self.service_details.get("type"),
            },
            "managed_ressource_details": {
                "id": self.managed_ressource_details.get("id"),
                "display_on_app": self.managed_ressource_details.get("display_on_app"),
                "is_custom": self.managed_ressource_details.get("is_custom"),
                "is_published": self.managed_ressource_details.get("is_published"),
                "plan_id": self.managed_ressource_details.get("plan_id"),
                "preparation_time": self.managed_ressource_details.get("preparation_time"),
                "price": self.managed_ressource_details.get("price"),
                "priority": self.managed_ressource_details.get("priority"),
                "service_id": self.managed_ressource_details.get("service_id"),
                "service_plan_type": self.managed_ressource_details.get("service_plan_type"),
                "subscription_category": self.managed_ressource_details.get(
                    "subscription_category"
                ),
                "unity": self.managed_ressource_details.get("unity"),
            },
        }
