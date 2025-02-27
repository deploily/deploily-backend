# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_login import current_user
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy.sql import exists
from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Service(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String(255))
    description = Column(String(255), nullable=False)
    specifications = Column(String(255))
    documentation_url = Column(String(255), nullable=False)
    unit_price = Column(Float)
    service_url = Column(String(255), nullable=False)
    image_service = Column(ImageColumn)
    parameters = relationship("Parameter")
    cart_lines = relationship("CartLine", overlaps="service")
    myfavorites = relationship("MyFavorites", overlaps="service")
    is_favorite = Column(Boolean)

    @property
    def is_favorite(self):
        return True if len(self.myfavorites)>0 else False

    
    def __repr__(self):
        return self.name
