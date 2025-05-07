# -*- coding: utf-8 -*-

from sqlalchemy import Column, Text

from app.core.models import Service


class CicdService(Service):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "cicd_service"}

    cicd_field = Column(Text)

    def __repr__(self):
        return f"CicdService: {self.name} "
