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

    credits = Column(Float, default=0)
    phone = Column(String)
    subscriptions = relationship(
        "MyService", backref="user", foreign_keys="MyService.user_id")

    @property
    def existing_subscription(self):
        """Retourne True si l'utilisateur a un abonnement actif"""
        latest_subscription = (
            db.session.query(MyService)
            .filter_by(user_id=self.id)
            .order_by(MyService.start_date.desc())
            .first()
        )

        if not latest_subscription:
            return False

        expiration_date = latest_subscription.start_date.replace(day=1) + timedelta(
            days=latest_subscription.duration_month * 30
        )

        return expiration_date > datetime.now().date()
