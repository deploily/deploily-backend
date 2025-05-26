# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from app import db
from app.core.models.my_favorites_models import MyFavorites

# from app.service_api.models.api_services_model import ApiService
from app.utils.utils import get_user


class Service(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String(255))
    description = Column(Text, nullable=False)
    specifications = Column(Text)
    documentation_url = Column(String(255), nullable=False)
    unit_price = Column(Float)
    image_service = Column(ImageColumn)
    tags = relationship(
        "ServiceTag", secondary="service_tag_association", back_populates="services"
    )
    service_plans = relationship("ServicePlan")
    myfavorites = relationship("MyFavorites", back_populates="service", overlaps="service")
    ratings = relationship("Score", back_populates="service", overlaps="service")
    comments = relationship("Comment", back_populates="service", overlaps="service")
    service_slug = Column(String(255), default="temp-slug")
    type = Column(String(50), default="service", nullable=False)

    __mapper_args__ = {"polymorphic_identity": "service", "polymorphic_on": type}

    @property
    def is_in_favorite(self):

        user = get_user()
        if not user.is_authenticated:
            return False
        favori = (
            db.session.query(MyFavorites)
            .filter_by(service_id=self.id, created_by_fk=user.id)
            .first()
        )

        return favori is not None

    @property
    def service_details(self):
        service_json = {}

        # Skip if it's the base class

        # Get all keys from the base (Service)
        base_keys = set(Service.__mapper__.c.keys())

        # Get all keys from the subclass
        child_keys = set(self.__class__.__mapper__.c.keys())

        # Only use keys that are in child but not in base
        specific_child_keys = child_keys - base_keys

        for key in specific_child_keys:
            try:
                service_json[key] = getattr(self, key)
            except Exception:
                service_json[key] = None

        return service_json

    def __repr__(self):
        return self.name
