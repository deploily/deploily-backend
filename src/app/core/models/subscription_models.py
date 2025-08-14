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
    case,
    event,
    func,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from app.utils.utils import get_user

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
    is_upgrade = Column(Boolean, default=False)
    is_renew = Column(Boolean, default=False)
    managed_ressource_id = Column(Integer, ForeignKey("managed_ressource.id"))
    managed_ressource = relationship("ManagedRessource", back_populates="subscriptions")
    type = Column(String(50), default="subscription")
    __mapper_args__ = {"polymorphic_identity": "subscription", "polymorphic_on": type}

    @property
    def is_subscribed(self):
        user = get_user()
        if not user.is_authenticated:
            return False

        # When the subscription is just created and still linked to this object
        if self.status == "active" and not self.is_expired:
            return True

        subscription = (
            db.session.query(Subscription)
            .filter(
                Subscription.service_plan.has(service_id=self.id),
                Subscription.created_by_fk == user.id,
                Subscription.status == "active",
            )
            .first()
        )

        return subscription is not None and not subscription.is_expired

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
            service_json["is_subscribed"] = self.is_subscribed

            return service_json

        else:
            _logger.warning("Service or service_plan is None for MyService ID %d", self.id)
            return {}

    @property
    def managed_ressource_details(self):

        if self.managed_ressource and self.managed_ressource.ressource_service_plan:
            ressource_service_plan = self.managed_ressource.ressource_service_plan
            managed_ressource = {}
            # Get all keys from the base (Service)
            # base_keys = set(Service.__mapper__.c.keys())

            # Get all keys from the subclass
            child_keys = set(ressource_service_plan.__class__.__mapper__.c.keys())

            # Only use keys that are in child but not in base
            specific_child_keys = child_keys

            for key in specific_child_keys:
                try:
                    managed_ressource[key] = getattr(ressource_service_plan, key)
                except Exception:
                    managed_ressource[key] = None
            # for key, value in service.__dict__.items():
            #     if not key.startswith("_"):
            #         service_json[key] = value
            return managed_ressource

        else:
            _logger.warning("Service or service_plan is None for MyService ID %d", self.id)
            return {}

    @property
    def service_name(self):
        details = self.service_details
        return details.get("name") if isinstance(details, dict) else None

    # @property
    # def is_expired(self):
    #     is_subscription_expired = False
    #     if self.start_date + relativedelta(months=self.duration_month) < datetime.now():
    #         is_subscription_expired = True
    #     return is_subscription_expired

    @hybrid_property
    def is_expired(self):
        if self.start_date and self.duration_month:
            return self.start_date + relativedelta(months=self.duration_month) < datetime.utcnow()
        return False

    @is_expired.expression
    def is_expired(cls):
        return case(
            [
                (
                    cls.start_date.isnot(None),
                    func.now()
                    > (
                        func.date_trunc("second", cls.start_date)
                        + func.make_interval(months=cls.duration_month)
                    ),
                )
            ],
            else_=False,
        )

    def __repr__(self):
        # return str(self.id)
        return f"{self.service_plan} | {self.created_by} ({self.profile.name})"


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
