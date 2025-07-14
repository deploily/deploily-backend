# -*- coding: utf-8 -*-
import logging

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, Enum, Integer, String, Text
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
    category_type = Column(
        Enum(
            "vps",
            "messagerie",
            "stockage_objet_s3",
            "backup_vps",
            "dedicated_server",
            "web_hosting",
            name="category_type",
        ),
        default="vps",
    )

    @property
    def list_providers(self):
        provider_data = {}

        for service in self.ressouce_services:
            provider = service.provider
            if provider:
                if provider.id not in provider_data:
                    provider_data[provider.id] = {
                        "name": provider.name,
                        "website": provider.website,
                        "logo": provider.logo,
                        "min_price": None,
                    }

                for plan in service.service_plans:
                    if plan.price is not None:
                        current_min = provider_data[provider.id]["min_price"]
                        if current_min is None or plan.price < current_min:
                            provider_data[provider.id]["min_price"] = plan.price

        return list(provider_data.values())

    @property
    def min_category_price(self):
        all_prices = [
            plan.price
            for service in self.ressouce_services
            for plan in service.service_plans
            if plan.price is not None
        ]
        return min(all_prices) if all_prices else None

    def __repr__(self):
        return self.name
