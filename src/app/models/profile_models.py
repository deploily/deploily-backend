# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, ImageColumn
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Float

from sqlalchemy.orm import relationship, validates


class Profile(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    balance = Column(Float, default=0.0)
    type = Column(Enum("default", "personal", "company", name="type"))
    phone = Column(String, nullable=True)
    company_name = Column(String(255), nullable=True)
    company_registration_number = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship("MyUser", back_populates="profiles")

    def __repr__(self):
        return f"{self.name}"
