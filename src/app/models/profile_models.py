# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, ImageColumn
from sqlalchemy import Column, ForeignKey, Integer, String, Enum

from sqlalchemy.orm import relationship


class Profile(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type = Column(Enum("default", "personal", "company", name="type"))

    user_id = Column(Integer, ForeignKey("ab_user.id"))  
    user = relationship("MyUser", back_populates="profiles")  

    def __repr__(self):
        return f"{self.name}"
