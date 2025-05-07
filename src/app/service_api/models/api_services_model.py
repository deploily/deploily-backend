# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Text

from app.core.models import Service


class ApiService(Service):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "api_service"}

    curl_command = Column(Text)
    service_url = Column(String(255), nullable=False)
    api_playground_url = Column(String(255), nullable=False)

    def __repr__(self):
        return f"ApiService: {self.name} "
