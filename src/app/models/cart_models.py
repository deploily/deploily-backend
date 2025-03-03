# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Enum, Float, Integer
from sqlalchemy.orm import relationship


class Cart(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    status = Column(Enum("draft", "confirm", name="status"))
    total_amount = Column(Float)
    cart_lines = relationship("CartLine", back_populates="cart")

    def __repr__(self):
        return str(self.id)
