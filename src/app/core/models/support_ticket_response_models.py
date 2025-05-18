# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class SupportTicketResponse(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    message = Column(String(255))
    support_ticket_id = Column(Integer, ForeignKey("support_ticket.id"))
    support_ticket = relationship("SupportTicket", cascade="all,delete")

    def __repr__(self):
        return str(self.id)
