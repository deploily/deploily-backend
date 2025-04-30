# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Enum, Integer, String


class Mail(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(String, default="")
    mail_state = Column(Enum("outGoing", "sent", "error", "canceled", name="mail_state"))
    email_from = Column(String(255), default="")
    email_to = Column(String(255), default="")

    def __repr__(self):
        return str(self.id)
