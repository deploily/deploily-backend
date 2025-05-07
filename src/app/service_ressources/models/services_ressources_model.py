# -*- coding: utf-8 -*-

from sqlalchemy import Column, Text

from app.core.models import Service


class RessourceService(Service):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "ressource_service"}

    ressource_field = Column(Text)

    def __repr__(self):
        return f"RessourceService: {self.name} "
