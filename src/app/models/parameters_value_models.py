# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ParameterValue(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False)
    parameter_id = Column(Integer, ForeignKey("parameter.id"))
    parameter = relationship("Parameter", cascade="all,delete")
    name = Column(String(255))
    cart_line_id = Column(Integer, ForeignKey("cart_line.id"))
    cart_line = relationship("CartLine", cascade="all,delete")


    @property
    def name(self):
        return self.parameter.name if self.parameter else None

    def __repr__(self):
        return str(self.id)
