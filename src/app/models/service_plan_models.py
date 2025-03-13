# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column, Float, Integer, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from app import appbuilder, db
from flask_appbuilder.models.decorators import renders
from datetime import datetime


class ServicePlan(Model):
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    limit = Column(String)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")
    plan_id = Column(Integer, ForeignKey("plan.id"))
    plan = relationship("Plan")
    ubscription_category = Column(
        Enum("monthly", "yearly", name="subscription_category"))
    options = relationship(
        "ServicePlanOption", back_populates="service_plan")

   
    def __repr__(self):
        return str(self.id)
