# app/core/models/service_plan_models.py
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.models.service_plan_service_plan_option_association import (
    service_plan_option_association,
)


class ServicePlan(Model):
    id = Column(Integer, primary_key=True)
    price = Column(Float)

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")

    plan_id = Column(Integer, ForeignKey("plan.id"))
    plan = relationship("Plan")

    is_custom = Column(Boolean, default=False)
    subscription_category = Column(Enum("monthly", "yearly", name="subscription_category"))

    options = relationship(
        "ServicePlanOption",
        secondary=service_plan_option_association,
        back_populates="service_plans",
    )

    def __repr__(self):
        return f"{self.service} | {self.plan}"
