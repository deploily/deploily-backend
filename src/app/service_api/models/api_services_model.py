# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.core.models import Service


class ApiService(Service):

    __tablename__ = "api_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "api_service",
    }

    curl_command = Column(Text)
    service_url = Column(String(255))
    api_playground_url = Column(String(255))

    def __repr__(self):
        return f"ApiService: {self.name} "
