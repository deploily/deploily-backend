# app/core/models/service_plan_models.py
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.models.service_plan_option_models import ServicePlanOption
from app.core.models.service_plan_service_plan_option_association import (
    service_plan_option_association,
)


class ServicePlan(Model):
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    preparation_time = Column(Integer, nullable=False)

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")

    plan_id = Column(Integer, ForeignKey("plan.id"))
    plan = relationship("Plan")

    is_custom = Column(Boolean, default=False)
    subscription_category = Column(Enum("monthly", "yearly", name="subscription_category"))
    service_plan_type = Column(Enum("ressource", "app", "api", "deployment", name="plan_type"))
    is_published = Column(Boolean, default=False)
    display_on_app = Column(Boolean, default=False)
    unity = Column(String)
    priority = Column(Integer, default=0)
    managed_ressources = relationship("ManagedRessource", back_populates="ressource_service_plan")

    options = relationship(
        "ServicePlanOption",
        secondary=service_plan_option_association,
        back_populates="service_plans",
        order_by=ServicePlanOption.sequence,
    )

    @property
    def provider_info(self):
        if (
            self.service
            and getattr(self.service, "provider", None)
            and self.service.__class__.__name__ == "RessourceService"
        ):
            provider = self.service.provider
            return {
                "name": provider.name,
                "website": provider.website,
                "logo": provider.logo,
            }
        return None

    def __repr__(self):
        return f"{self.service} | {self.plan}"
