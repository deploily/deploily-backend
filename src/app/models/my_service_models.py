# -*- coding: utf-8 -*-
from datetime import datetime

from cryptography.fernet import Fernet
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, event

# FERNET_KEY = Fernet.generate_key()  # Change this in production
FERNET_KEY = b"nSJDjmxhCOb06hbOxzBT6eskGiZAnwh6iUVI5uaP0is="  # Change this in production
print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", FERNET_KEY)
encryptor = Fernet(FERNET_KEY)  # Create a single Fernet instance


class MyService(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(
        DateTime,
        default=lambda: datetime.now().replace(microsecond=0),
        nullable=False,
    )
    amount = Column(Float)
    duration_month = Column(Integer)
    # Store encrypted password in the database
    encrypted_password = Column("encrypted_password", String(255), nullable=False)

    is_encrypted = Column(Boolean, default=False)  # Flag to check if password is encrypted

    def __repr__(self):
        return str(self.id)


@event.listens_for(MyService, "before_insert")
@event.listens_for(MyService, "before_update")
def encrypt_password_before_save(mapper, connection, target):
    """Ensure password is encrypted before saving."""
    if (
        target.encrypted_password
        and not target.encrypted_password.startswith("gAAAAA")
        and not target.is_encrypted
    ):
        print("Encrypting password in event listener...")
        target.encrypted_password = encryptor.encrypt(target.encrypted_password.encode()).decode()
        target.is_encrypted = True


@event.listens_for(MyService, "load")
def decrypt_password_on_load(target, context):
    """Decrypt password when loading the object from the database."""
    if target.encrypted_password and target.is_encrypted:
        try:
            target.encrypted_password = encryptor.decrypt(
                target.encrypted_password.encode()
            ).decode()
            print(f"Decrypted password on load: {target.encrypted_password}")  # Debugging
        except Exception as e:
            print(f"Decryption error: {e}")
            target.encrypted_password = None  # Set to None if decryption fails
