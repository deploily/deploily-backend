from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from flask import Markup, url_for


class MyUser(User):
    __tablename__ = "ab_user"
    
    
    phone = Column(String)
