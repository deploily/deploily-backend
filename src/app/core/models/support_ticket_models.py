# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, ImageColumn
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class SupportTicket(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text, nullable=False)
    image = Column(ImageColumn)
    status = Column(Enum("open", "closed", name="status"))
    subscription_id = Column(Integer, ForeignKey("subscription.id"))
    subscription = relationship("Subscription")
    support_ticket_responses = relationship("SupportTicketResponse")

    def __repr__(self):
        return f"[{self.id} | {self.status}] {self.title_shortened}"

    @property
    def title_shortened(self):
        _COL_LENGTH = 40
        return self.title[:_COL_LENGTH] + "..." if len(self.title) > _COL_LENGTH else self.title

    @property
    def responses_with_details(self):
        return [
            {
                "id": r.id,
                "message": r.message,
                "created_on": str(r.created_on),
                "created_by": (
                    {
                        "username": r.created_by.username,
                        "first_name": r.created_by.first_name,
                        "last_name": r.created_by.last_name,
                    }
                    if r.created_by
                    else None
                ),
            }
            for r in self.support_ticket_responses
        ]
