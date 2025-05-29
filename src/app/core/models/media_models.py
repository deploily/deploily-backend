# -*- coding: utf-8 -*-
import logging

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

_logger = logging.getLogger(__name__)


class Media(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    image = Column(ImageColumn)

    category_id = Column(Integer, ForeignKey("service_ressouce_category.id"), nullable=False)

    category = relationship("ServiceRessouceCategory", back_populates="medias")

    def __repr__(self):
        return self.title
