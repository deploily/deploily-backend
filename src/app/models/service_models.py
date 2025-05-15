# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import relationship

from app import db
from app.models.my_favorites_models import MyFavorites
from app.utils.utils import get_user

from config import DB_LANGUAGES

class Service(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String(255))
    curl_command = Column(Text)
    description = Column(Text, nullable=False)
    specifications = Column(Text)
    documentation_url = Column(String(255), nullable=False)
    unit_price = Column(Float)
    service_url = Column(String(255), nullable=False)
    api_playground_url = Column(String(255), nullable=False)
    image_service = Column(ImageColumn)
    tags = relationship(
        "ServiceTag", secondary="service_tag_association", back_populates="services"
    )
    service_plans = relationship("ServicePlan")
    myfavorites = relationship("MyFavorites", back_populates="service", overlaps="service")
    type = Column(String(50), default="service", nullable=False)
    service_slug = Column(String(255), unique=True, default="temp-slug")

    for lang in DB_LANGUAGES:
        if lang != 'en':
            locals()[f'description_{lang}'] = Column(Text, nullable=True)
            locals()[f'short_description_{lang}'] = Column(String(255), nullable=True)
            locals()[f'specifications_{lang}'] = Column(Text, nullable=True)

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
