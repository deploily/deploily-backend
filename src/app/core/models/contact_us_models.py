# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ContactUs(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    ressource_id = Column(Integer, ForeignKey("ressource_service.id"))
    ressource = relationship("RessourceService", back_populates="contact_us")

    def __repr__(self):
        return self.name
