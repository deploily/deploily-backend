# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Text


class ApiToken(Model):
    id = Column(Integer, primary_key=True)
    token = Column(Text, nullable=False)
    partner = Column(String(100))
    token_prefix = Column(String(50))

    def __repr__(self):
        return f"ApiToken(id={self.id})"
