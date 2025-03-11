# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Float, Integer, DateTime, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import appbuilder, db
from datetime import datetime


class ServicePlan(Model):
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    limit = Column(Integer)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")
    ubscription_category = Column(
        Enum("monthly", "yearly", name="subscription_category"))

    def __repr__(self):
        return str(self.id)
