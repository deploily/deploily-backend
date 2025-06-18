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
    image = Column(ImageColumn(size=(500, 300, True), thumbnail_size=(30, 30, True)))

    horizontal_image = Column(ImageColumn(size=(1200, 628, True), thumbnail_size=(60, 31, True)))
    vertical_image = Column(ImageColumn(size=(1080, 1350, True), thumbnail_size=(54, 68, True)))
    square_image = Column(ImageColumn(size=(1080, 1080, True), thumbnail_size=(60, 60, True)))

    category_id = Column(Integer, ForeignKey("service_ressouce_category.id"))
    category = relationship("ServiceRessouceCategory", back_populates="medias")

    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", back_populates="medias")

    def __repr__(self):
        return self.title
