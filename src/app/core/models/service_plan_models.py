# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship


class ServicePlan(Model):
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")
    plan_id = Column(Integer, ForeignKey("plan.id"))
    plan = relationship("Plan")
    subscription_category = Column(Enum("monthly", "yearly", name="subscription_category"))
    options = relationship("ServicePlanOption", back_populates="service_plan")

    def __repr__(self):
        return str(self.id)
