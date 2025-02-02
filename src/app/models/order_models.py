# -*- coding: utf-8 -*-
# TODO 3

# TODO Add model
# TODO Add Field Status = [DRAFT, DONE] + 
# TODO Add Field service Many2One  to Services 
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

class Order(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    status = Column(Enum("draft", "done", name="status"))
    service = relationship("Service")
    
    def __repr__(self):
            return self.name