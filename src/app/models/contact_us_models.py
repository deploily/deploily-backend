# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer, String


class ContactUs(Model, AuditMixin):
    __tablename__ = "contact_us"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "contact_us",  #
        "polymorphic_on": type,
    }

    def __repr__(self):
        return f"{self.name} - {self.type}"


class SupportContact(ContactUs):
    __tablename__ = "support_contact"
    id = Column(Integer, ForeignKey("contact_us.id"), primary_key=True)
    issue_type = Column(String(255), nullable=True)

    __mapper_args__ = {"polymorphic_identity": "support_contact"}


class FeedbackContact(ContactUs):
    __tablename__ = "feedback_contact"
    id = Column(Integer, ForeignKey("contact_us.id"), primary_key=True)
    rating = Column(Integer, nullable=True)

    __mapper_args__ = {"polymorphic_identity": "feedback_contact"}
