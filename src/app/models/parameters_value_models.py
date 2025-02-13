# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from flask_appbuilder.models.mixins import AuditMixin


class ParameterValue(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False)
    parameter_id = Column(Integer, ForeignKey("parameter.id"))
    parameter = relationship("Parameter", cascade="all,delete")
    cart_line_id = Column(Integer, ForeignKey("cart_line.id"))
    cart_line = relationship("CartLine", cascade="all,delete")

    def __repr__(self):
        return self.amount
