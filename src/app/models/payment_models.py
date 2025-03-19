# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Float,Enum
from sqlalchemy.orm import relationship


class Payment(Model):
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    payment_method = Column(Enum("card","bank_transfer"), nullable=False)         
    subscription_id = Column(Integer, ForeignKey("subscribe.id"), nullable=False)
    subscription = relationship("Subscribe", back_populates="payments")
    status = Column(Enum("pending", "completed", "failed"), default="pending")

    def __repr__(self):
        return str(self.id)
