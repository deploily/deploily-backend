# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from datetime import date
from sqlalchemy import Column, Integer, DateTime, Enum, Boolean, String
from sqlalchemy.orm import relationship


class PromoCode(Model):
    id = Column(Integer, primary_key=True)
    code = Column(String)
    rate = Column(Integer)
    expiration_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    usage_type = Column(Enum("single_use", "multiple_use",
                        name="promo_usage_type"), default="single_use")

    @property
    def is_valid(self):
        """ Check if the promo code is still valid """
        return self.expiration_date.date() >= date.today()

    def __repr__(self):
        return str(self.id)
