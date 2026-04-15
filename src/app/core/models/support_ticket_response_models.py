# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship


class SupportTicketResponse(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    support_ticket_id = Column(Integer, ForeignKey("support_ticket.id"))
    support_ticket = relationship("SupportTicket", cascade="all,delete")
    status = Column(
        Enum("pending", "sent", "seen", "rejected", name="support_ticket_response_status"),
        default="pending",
        nullable=False,
    )

    def __repr__(self):
        return f"[{self.id} | {self.status}] {self.message_shortened}"

    @property
    def message_shortened(self):
        _COL_LENGTH = 40
        return (
            self.message[:_COL_LENGTH] + "..." if len(self.message) > _COL_LENGTH else self.message
        )
