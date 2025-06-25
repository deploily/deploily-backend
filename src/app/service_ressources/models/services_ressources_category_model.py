# -*- coding: utf-8 -*-
import logging

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

_logger = logging.getLogger(__name__)


class ServiceRessouceCategory(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String(255))
    description = Column(Text, nullable=False)
    logo = Column(ImageColumn)
    ressouce_services = relationship("RessourceService", back_populates="ressouce_category")
    medias = relationship("Media", back_populates="category", cascade="all, delete-orphan")

    @property
    def list_providers(self):
        unique_providers = {}
        for service in self.ressouce_services:
            provider = service.provider
            if provider and provider.id not in unique_providers:
                min_price = min(
                    (plan.price for plan in service.service_plans if plan.price is not None),
                    default=None,
                )
                unique_providers[provider.id] = {
                    "name": provider.name,
                    "website": provider.website,
                    "logo": provider.logo,
                    "min_price": min_price,
                }
        return list(unique_providers.values())

    @property
    def min_category_price(self):
        for service in self.ressouce_services:
            min_price = min(
                (plan.price for plan in service.service_plans if plan.price is not None),
                default=None,
            )
            return min_price if min_price is not None else None

    def __repr__(self):
        return self.name
