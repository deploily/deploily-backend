# -*- coding: utf-8 -*-
from datetime import datetime

from flask_appbuilder import Model

from flask_appbuilder.models.mixins import AuditMixin, ImageColumn
from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Payment(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(
        Enum("pending", "completed", "failed", name="status_payment"), default="pending"
    )
    start_date = Column(DateTime, default=lambda: datetime.now().replace(microsecond=0))
    payment_method = Column(
        Enum("card", "bank_transfer", "cloud_credit", name="payment_method_enum"), nullable=False
    )
    profile_id = Column(Integer, ForeignKey("payment_profile.id"), nullable=False)
    profile = relationship("PaymentProfile")
    subscription_id = Column(Integer, ForeignKey("subscription.id"))
    subscription = relationship("Subscription", back_populates="payments", overlaps="payments")

    payment_receipt = Column(ImageColumn, nullable=True)
    satim_order_id = Column(String)
    order_id = Column(String)

    def __repr__(self):
        return str(self.id)
