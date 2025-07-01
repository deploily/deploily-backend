# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class ApiToken(Model):
    id = Column(Integer, primary_key=True)
    token = Column(Text, nullable=False)
    token_prefix = Column(String(50))
    partner_id = Column(Integer, ForeignKey("ab_user.id"), nullable=False)
    partner = relationship("User", backref="api_tokens")
    rate = Column(Integer, nullable=False)

    def __repr__(self):
        return f"{self.token}"
