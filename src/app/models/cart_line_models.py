# -*- coding: utf-8 -*-
from datetime import datetime

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship


class CartLine(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    start_date = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
        nullable=False,
    )
    amount = Column(Float)
    duration_month = Column(Integer)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service", overlaps="cart_lines")
    cart_id = Column(Integer, ForeignKey("cart.id"))
    cart = relationship("Cart", back_populates="cart_lines")
    parameters_values = relationship("ParameterValue")

    def __repr__(self):
        return str(self.id)
