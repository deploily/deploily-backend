# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Comment(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    comment = Column(String(255), nullable=False)
    service_id = Column(Integer, ForeignKey("service.id"))
    service = relationship("Service")
    status = Column(
        Enum("pending", "approved", "rejected", "spam", name="comment_status"),
        default="pending",
        nullable=False,
    )

    def __repr__(self):
        return str(self.id)
