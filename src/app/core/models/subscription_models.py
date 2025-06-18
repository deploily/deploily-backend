# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from cryptography.fernet import Fernet
from dateutil.relativedelta import relativedelta
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    event,
)
from sqlalchemy.orm import relationship

# from app.core.models.service_models import Service

FERNET_KEY = os.getenv("FERNET_KEY", "QkqrpIbcUuQ_5Ho25VEv5oPFN4IVuOYojOMwneVbZNQ=")

encryptor = Fernet(FERNET_KEY)


_logger = logging.getLogger(__name__)


class Subscription(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
        nullable=False,
    )
    total_amount = Column(Float)
    price = Column(Float)
    payment_status = Column(Enum("unpaid", "paid", name="payment_status"))
    duration_month = Column(Integer, default=0)
    status = Column(
        Enum("inactive", "active", name="subscription_status"),
        default="inactive",
    )
    service_plan_id = Column(Integer, ForeignKey("service_plan.id"))
    service_plan = relationship("ServicePlan")
    promo_code_id = Column(Integer, ForeignKey("promo_code.id"), nullable=True)
    promo_code = relationship("PromoCode", back_populates="subscriptions")
    api_key = Column("api_key", String(255))
    is_encrypted = Column(Boolean, default=False)
    payments = relationship("Payment", back_populates="subscription", overlaps="subscription")
    profile_id = Column(Integer, ForeignKey("payment_profile.id"))
    profile = relationship("PaymentProfile")
    type = Column(String(50), default="subscription")
    __mapper_args__ = {"polymorphic_identity": "subscription", "polymorphic_on": type}

    @property
    def service_details(self):

        if self.service_plan and self.service_plan.service:
            service = self.service_plan.service
            service_json = {}
            # Get all keys from the base (Service)
            # base_keys = set(Service.__mapper__.c.keys())

            # Get all keys from the subclass
            child_keys = set(service.__class__.__mapper__.c.keys())

            # Only use keys that are in child but not in base
            specific_child_keys = child_keys

            for key in specific_child_keys:
                try:
                    service_json[key] = getattr(service, key)
                except Exception:
                    service_json[key] = None
            # for key, value in service.__dict__.items():
            #     if not key.startswith("_"):
            #         service_json[key] = value

            return service_json
        else:
            _logger.warning("Service or service_plan is None for MyService ID %d", self.id)
            return {}

    @property
    def is_expired(self):
        is_subscription_expired = False
        if self.start_date + relativedelta(months=self.duration_month) < datetime.now():
            is_subscription_expired = True
        return is_subscription_expired

    def __repr__(self):
        return str(self.id)


def encrypt_api_key(api_key):
    """Encrypt the given API key."""
    if api_key and not api_key.startswith("gAAAAA"):
        return encryptor.encrypt(api_key.encode()).decode()
    return api_key


def decrypt_api_key(api_key):
    """Decrypt the given API key."""
    try:
        return encryptor.decrypt(api_key.encode()).decode()
    except Exception as e:
        print(f"Decryption error: {e}")
        return None


@event.listens_for(Subscription, "before_insert")
@event.listens_for(Subscription, "before_update")
def encrypt_data_before_save(mapper, connection, target):
    """Ensure api_key is encrypted before saving."""
    target.is_encrypted = False

    if target.api_key and not target.is_encrypted:
        print("Encrypting api_key in event listener...")
        target.api_key = encrypt_api_key(target.api_key)
        target.is_encrypted = True


@event.listens_for(Subscription, "load")
def decrypt_data_on_load(target, context):
    """Decrypt api_key when loading the object from the database."""
    if target.api_key and target.is_encrypted:
        target.api_key = decrypt_api_key(target.api_key)
        if target.api_key:
            print(f"Decrypted api_key on load: {target.api_key}")
