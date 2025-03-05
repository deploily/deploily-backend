# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Float, Integer,DateTime,String
from sqlalchemy.orm import relationship
from app import appbuilder, db
from datetime import datetime

from flask_appbuilder.models.mixins import ImageColumn
from flask_login import current_user
from app.models.my_favorites_models import MyFavorites
from flask_appbuilder.security.sqla.models import User


class MyService(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name= Column(String)
    start_date = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
        nullable=False,
    )
    amount = Column(Float)
    duration_month = Column(Integer)

    def __repr__(self):
        return str(self.id)