# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship


class PromoCode(Model):
    id = Column(Integer, primary_key=True)
    rate = Column(Integer)
    expiration_date = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    usage_type = Column(Enum("single_use", "multiple_use",
                        name="promo_usage_type"), default="single_use")
    usages = relationship("PromoUsage")

    def __repr__(self):
        return str(self.id)
