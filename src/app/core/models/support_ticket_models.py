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


# @event.listens_for(SupportTicket, "before_update")
# def before_update(mapper, connection, target):
#     """
#     Ensure changed_by_fk is ALWAYS set.
#     Works for:
#     - HTTP requests
#     - Background jobs (APScheduler)
#     """

#     user_id = None

#     # Case 1: HTTP request context
#     try:
#         user = getattr(g, "user", None)
#         if user and getattr(user, "is_authenticated", False):
#             user_id = user.id
#     except RuntimeError:
#         # No app context → scheduler
#         pass

#     # Case 2: scheduler / background task
#     if not user_id:
#         user_id = 1

#     target.changed_by_fk = user_id
