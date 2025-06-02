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

    def __repr__(self):
        return self.name
