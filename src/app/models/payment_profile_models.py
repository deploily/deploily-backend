# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class PaymentProfile(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    balance = Column(Float, default=0.0)
    profile_type = Column(Enum("default", "personal", "company", name="profile_type"))
    phone = Column(String, nullable=True)
    is_company = Column(Boolean, default=False)
    company_name = Column(String(255), nullable=True)
    company_registration_number = Column(String(255), nullable=True)
    tax_article = Column(String(255), nullable=True)
    nif = Column(String(255), nullable=True)
    nis = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    wilaya = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    postal_code = Column(String(20), nullable=True)

    user_id = Column(Integer, ForeignKey("ab_user.id"))
    is_default_profile = Column(Boolean, default=False)
    user = relationship("MyUser", back_populates="profiles")

    def __repr__(self):
        return f"{self.name}"
