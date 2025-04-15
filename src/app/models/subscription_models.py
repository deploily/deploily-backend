# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from cryptography.fernet import Fernet
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
    duration_month = Column(Integer)
    status = Column(
        Enum("inactive", "active", name="subscription_status"),
        default="inactive",
    )
    is_expired = Column(Boolean, default=False)
    service_plan_id = Column(Integer, ForeignKey("service_plan.id"))
    service_plan = relationship("ServicePlan")
    promo_code_id = Column(Integer, ForeignKey("promo_code.id"), nullable=True)
    promo_code = relationship("PromoCode", back_populates="subscriptions")
    api_key = Column("api_key", String(255))
    is_encrypted = Column(Boolean, default=False)
    payments = relationship("Payment", back_populates="subscription", overlaps="subscription")
    profile_id = Column(Integer, ForeignKey("payment_profile.id"))
    profile = relationship("PaymentProfile")

    @property
    def service_details(self):

        if self.service_plan and self.service_plan.service:
            service = self.service_plan.service

            service_json = {}
            for key, value in service.__dict__.items():

                if not key.startswith("_"):
                    service_json[key] = value

            return service_json
        else:
            _logger.warning("Service or service_plan is None for MyService ID %d", self.id)
            return {}

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
