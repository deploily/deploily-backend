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
    providers = relationship("ProvidersRessourceService", back_populates="ressource_service")

    def __repr__(self):
        return f"RessourceService: {self.name} "
