# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import relationship

class Service(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    documentation_url = Column(String(255), nullable=False)
    unit_price = Column(Float)
    service_url=Column(String(255), nullable=False)
    image_service = Column(ImageColumn)
    parameters = relationship("ServiceParameters")
    
    def __repr__(self):
            return self.name
