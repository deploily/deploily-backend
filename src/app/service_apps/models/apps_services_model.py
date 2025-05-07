# -*- coding: utf-8 -*-

from sqlalchemy import Column, Text

from app.core.models import Service


class AppService(Service):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "app_service"}

    apps_field = Column(Text)

    def __repr__(self):
        return f"AppService: {self.name} "
