# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ParameterValue(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False)
    parameter_id = Column(Integer, ForeignKey("parameter.id"))
    parameter = relationship("Parameter")
    subscribe_id = Column(Integer, ForeignKey("subscribe.id"))
    subscribe = relationship("Subscribe")

    def __repr__(self):
        return str(self.id)
