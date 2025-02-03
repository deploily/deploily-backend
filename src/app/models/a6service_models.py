# -*- coding: utf-8 -*-
# TODO 4

# TODO Add model
# TODO Add Field upstream_id, ....

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

class A6Service(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    upstream_id =Column(Integer)
    cart_id = Column(Integer, ForeignKey("cart.id"))
    cart = relationship("Cart",cascade="all,delete",)

    def __repr__(self):
            return self.name
