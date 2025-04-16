# -*- coding: utf-8 -*-
import logging

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Boolean, Column, Enum, Float, Integer, String
from sqlalchemy.orm import relationship

from app import db
from app.models.payment_models import Payment
from app.models.subscription_models import Subscription

_logger = logging.getLogger(__name__)


class PaymentProfile(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255))
    balance = Column(Float, default=0.0)
    profile_type = Column(Enum("default", "personal", "company", name="profile_type"))
    phone = Column(String, nullable=True)
    is_company = Column(Boolean, default=False)
    company_name = Column(String(255), nullable=True)
    company_registration_number = Column(String(255), nullable=True)
    tax_article = Column(String(255), nullable=True)
    nif = Column(String(255), nullable=True)
    nis = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    wilaya = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    postal_code = Column(String(20), nullable=True)

    # user_id = Column(Integer, ForeignKey("ab_user.id"))
    is_default_profile = Column(Boolean, default=False)
    # user = relationship("MyUser", back_populates="profiles")
    subscriptions = relationship("Subscription", back_populates="profile", overlaps="profile")

    @property
    def balance(self):
        # """Compute balance"""
        balance_rate = 0.0
        # Payments that are not cloud_credit
        payments_amounts = (
            db.session.query(Payment.amount).filter_by(profile_id=self.id, status="completed").all()
        )
        # Sum payment amounts (they come as list of tuples)
        total_payments = sum([p.amount for p in payments_amounts])

        # Sum subscription amounts from already-loaded self.subscriptions
        subscriptions_amounts = (
            db.session.query(Subscription.total_amount).filter_by(profile_id=self.id).all()
        )
        total_subscriptions = sum([p.total_amount for p in subscriptions_amounts])
        # Compute balance
        balance_rate = total_payments - total_subscriptions
        return balance_rate if not None else 0.0

    def __repr__(self):
        return f"{self.name}"
