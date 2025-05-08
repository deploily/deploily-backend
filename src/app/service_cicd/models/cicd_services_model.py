# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.models import Service


class CicdService(Service):

    __tablename__ = "cicd_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "cicd_service",
    }
    cicd_field = Column(Text)

    def __repr__(self):
        return f"CicdService: {self.name} "
