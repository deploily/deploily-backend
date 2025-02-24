# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Integer
from sqlalchemy import Float


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
    service = relationship(
        "Service", cascade="all,delete", overlaps="cart_lines")
    cart_id = Column(Integer, ForeignKey("cart.id"))
    cart = relationship("Cart", back_populates="cart_lines",
                        cascade="all,delete")
    parameters_values = relationship("ParameterValue")

    def __repr__(self):
        return str(self.id)
