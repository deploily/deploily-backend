# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, Text


class ApiToken(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    token = Column(Text, nullable=False)

    def __repr__(self):
        return f"ApiToken(id={self.id})"
