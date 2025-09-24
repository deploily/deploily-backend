# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ContactUs(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", back_populates="contact_us")

    partner_id = Column(Integer, ForeignKey("ab_user.id"), nullable=True)
    partner = relationship("User", backref="contact_us")

    def __repr__(self):
        return self.name
