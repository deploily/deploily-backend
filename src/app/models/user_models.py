# -*- coding: utf-8 -*-

from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from flask import Markup, url_for
from datetime import datetime, timedelta
from app.models.my_service_models import MyService
from app import appbuilder, db


class MyUser(User):
    __tablename__ = "ab_user"

    profiles = relationship("Profile")
    phone = Column(String)
