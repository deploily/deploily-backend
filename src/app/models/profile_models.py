# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, ImageColumn
from sqlalchemy import Column, ForeignKey, Integer, String, Enum

from sqlalchemy.orm import relationship, validates


class Profile(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type = Column(Enum("default", "personal", "company", name="type"))
    phone = Column(String, nullable=True)
    company_name = Column(String(255), nullable=True)
    company_registration_number = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship("MyUser", back_populates="profiles")

    def __repr__(self):
        return f"{self.name}"

    @validates("phone", "company_name", "company_registration_number")
    def validate_fields(self, key, value):
        """
        Vérifie que les champs sont bien associés au bon type de profil.
        """
        if not hasattr(self, "type") or self.type is None:
            return value

        if self.type == "default" and key in ["phone", "company_name", "company_registration_number"]:
            raise ValueError(f"The 'default' profile cannot have{key}")

        if self.type == "personal" and key in ["company_name", "company_registration_number"]:
            raise ValueError(f"The 'personal' profile cannot have {key}")

        if self.type == "company" and key == "phone":
            raise ValueError(f"The 'company' profile cannot have{key}")

        return value
