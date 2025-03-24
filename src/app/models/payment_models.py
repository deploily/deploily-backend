# -*- coding: utf-8 -*-
from datetime import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Payment(Model):
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(Enum("pending", "completed", "failed"), default="pending")
    start_date = Column(DateTime, default=lambda: datetime.now().replace(microsecond=0))
    payment_method = Column(
        Enum("card", "bank_transfer", name="payment_method_enum"), nullable=False
    )
    profile_id = Column(Integer, ForeignKey("profile.id"), nullable=False)
    profile = relationship("Profile")
    subscription_id = Column(Integer, ForeignKey("subscribe.id"), nullable=False)
    subscription = relationship("Subscribe", back_populates="payments", overlaps="payments")

    def __repr__(self):
        return str(self.id)
