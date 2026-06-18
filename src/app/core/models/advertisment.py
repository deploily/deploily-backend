# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Boolean, Column, Enum, Integer, String, Text


class Advertisement(Model):
    __tablename__ = "advertisement"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255))
    url = Column(String(255))
    url_label = Column(String(255))
    featured = Column(Boolean, default=False)
    image_1920 = Column(ImageColumn)
    image_128 = Column(ImageColumn)
    description = Column(Text)
    color = Column(String(255))
    AdvertisementType = Column(Enum("dashboard", "service", name="advertisement_type"))
