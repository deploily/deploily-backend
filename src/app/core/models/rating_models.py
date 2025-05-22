# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Rating(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    Rating = Column(Integer)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")

    def __repr__(self):
        return str(self.id)
