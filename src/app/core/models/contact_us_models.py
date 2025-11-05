# -*- coding: utf-8 -*-

from datetime import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
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
    internal_note = Column(Text, nullable=True)

    contact_us_status = Column(Enum("pending", "lead", "junk", name="contact_us_status"))
    created_on = Column(DateTime, default=lambda: datetime.now(), nullable=False)

    def __repr__(self):
        return self.name
