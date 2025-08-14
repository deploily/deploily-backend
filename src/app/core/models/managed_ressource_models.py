# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ManagedRessource(Model):
    __tablename__ = "managed_ressource"

    id = Column(Integer, primary_key=True)
    ip = Column(String(100), nullable=False)  # e.g. "v1.0.0"
    host_name = Column(String(100))
    operator_system = Column(String(100))
    subscriptions = relationship(
        "Subscription", back_populates="managed_ressource", cascade="all, delete-orphan"
    )
    ressource_service_plan = relationship("ServicePlan", back_populates="managed_ressources")
    ressource_service_plan_id = Column(Integer, ForeignKey("service_plan.id"))

    def __repr__(self):
        return f"{self.host_name} ({self.ip})"
