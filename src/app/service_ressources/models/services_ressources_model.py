# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.models import Service


class RessourceService(Service):
    __tablename__ = "ressource_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "ressource_service",
    }

    ressource_field = Column(Text)
    provider_id = Column(Integer, ForeignKey("providers_ressource_service.id"))
    discount = Column(Integer)
    provider = relationship("ProvidersRessourceService", back_populates="ressource_services")
    ressouce_category_id = Column(Integer, ForeignKey("service_ressouce_category.id"))
    ressouce_category = relationship("ServiceRessouceCategory", back_populates="ressouce_services")

    def __repr__(self):
        return f"{self.provider} / {self.name}"
