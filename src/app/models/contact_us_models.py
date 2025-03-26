# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String


class ContactUs(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name
