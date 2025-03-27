# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, ImageColumn
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class SupportTicket(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(String(255), nullable=False)
    image = Column(ImageColumn)
    status = Column(Enum("open", "closed", name="status"))
    subscribe_id = Column(Integer, ForeignKey("subscribe.id", ondelete="CASCADE"))
    subscribe = relationship("Subscribe")
    support_ticket_responses = relationship("SupportTicketResponse", cascade="all, delete")

    def __repr__(self):
        return f"{self.title}"
