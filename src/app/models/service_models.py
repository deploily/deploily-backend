# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app import appbuilder, db
from flask_appbuilder.models.mixins import ImageColumn
from flask_login import current_user
from app.models.my_favorites_models import MyFavorites
from flask_appbuilder.security.sqla.models import User


class Service(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String(255))
    description = Column(String(255), nullable=False)
    specifications = Column(String(255))
    documentation_url = Column(String(255), nullable=False)
    unit_price = Column(Float)
    service_url = Column(String(255), nullable=False)
    image_service = Column(ImageColumn)
    parameters = relationship("Parameter")
    cart_lines = relationship("CartLine", overlaps="service")
    myfavorites = relationship(
        "MyFavorites", back_populates="service", overlaps="service"
    )

    @property
    def is_in_favorite(self):

        user = current_user
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
