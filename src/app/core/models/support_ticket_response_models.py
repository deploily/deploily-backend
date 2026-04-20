# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from markupsafe import Markup
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

    def send_button(self):
        if self.support_ticket is None:
            return Markup(
                '<span class="badge" style="background-color:#ffc107;color:#000">No Ticket</span>'
            )

        if self.support_ticket.created_by_fk == self.created_by_fk:
            return Markup(
                '<span class="badge" style="background-color:#6c757d;color:#fff">Own Response</span>'
            )

        if self.status == "sent":
            return Markup(
                '<span class="badge" style="background-color:#28a745;color:#fff">Sent</span>'
            )

        if self.status == "rejected":
            return Markup(
                '<span class="badge" style="background-color:#dc3545;color:#fff">Rejected</span>'
            )

        return Markup(
            f'<form action="/admin/supportticket-response/{self.id}/send" method="POST">'
            f'<button type="submit" class="btn btn-sm btn-primary">'
            f'<i class="fa fa-paper-plane"></i> Send'
            f"</button></form>"
        )
