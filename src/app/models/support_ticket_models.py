# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin,ImageColumn
from sqlalchemy import Column, ForeignKey, Integer, String,Enum

from sqlalchemy.orm import relationship


class SupportTicket(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(255), nullable=False)
    image = Column(ImageColumn)
    status = Column(Enum("open", "closed", name="status"))
    cart_line_id = Column(Integer, ForeignKey("cart_line.id"))
    cart_line = relationship("CartLine", cascade="all,delete")

    def __repr__(self):
        return str(self.id)