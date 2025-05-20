# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Affiliation(Model, AuditMixin):
    id = Column(Integer, primary_key=True)

    total_price = Column(Float)
    affiliation_state = Column(Enum("pending", "confirmed", name="affiliation_state"))

    provider_id = Column(Integer, ForeignKey("providers_ressource_service.id"))
    provider = relationship("ProvidersRessourceService", back_populates="affiliations")

    service_plan_id = Column(Integer, ForeignKey("service_plan.id"))
    service_plan = relationship("ServicePlan")

    def __repr__(self):
        return f" {self.id} "
