# -*- coding: utf-8 -*-
import logging

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.models.service_models import Service

_logger = logging.getLogger(__name__)


class ServiceCategory(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String(255))
    description = Column(Text, nullable=False)
    services = relationship("Service", back_populates="category")

    @property
    def service_details(self):
        service_details_list = []

        # Clés de base définies dans la classe Service
        base_keys = set(Service.__mapper__.c.keys())

        for service in self.services:
            service_json = {}

            # Clés totales dans la classe réelle (enfant ou Service lui-même)
            all_keys = set()
            for base in service.__class__.__mapper__.iterate_to_root():
                all_keys.update(base.c.keys())

            # Obtenir seulement les clés spécifiques à l'enfant
            child_specific_keys = all_keys - base_keys

            for key in child_specific_keys:
                try:
                    service_json[key] = getattr(service, key)
                except Exception:
                    service_json[key] = None

            if service_json:
                service_details_list.append(service_json)

        return service_details_list

    def __repr__(self):
        return self.name
