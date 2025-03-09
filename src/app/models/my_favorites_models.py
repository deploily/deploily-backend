# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship


class MyFavorites(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service",overlaps="myfavorites")
    
    
    def __repr__(self):
        return str(self.id)
