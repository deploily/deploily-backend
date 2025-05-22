# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.models import Service


class AppService(Service):
    __tablename__ = "app_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "app_service",
    }

    apps_field = Column(Text)

    def __repr__(self):
        return f"AppService: {self.name} "
