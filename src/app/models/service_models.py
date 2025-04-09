# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app import db
from app.models.my_favorites_models import MyFavorites
from app.utils.utils import get_user


class Service(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String(255))
    curl_command = Column(String(255))
    description = Column(String(255), nullable=False)
    specifications = Column(String(255))
    documentation_url = Column(String(255), nullable=False)
    unit_price = Column(Float)
    service_url = Column(String(255), nullable=False)
    image_service = Column(ImageColumn)
    parameters = relationship("Parameter")
    tags = relationship("ServiceTag", overlaps="service")
    service_plans = relationship("ServicePlan")
    myfavorites = relationship("MyFavorites", back_populates="service", overlaps="service")
    type = Column(String(50), default="service", nullable=False)
    service_slug = Column(String(255), unique=True, default="temp-slug")

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

    def __repr__(self):
        return self.name
