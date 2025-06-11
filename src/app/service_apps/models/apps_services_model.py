# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from app import db
from app.core.models import Service
from app.core.models.rating_models import Score


class AppService(Service):
    __tablename__ = "app_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "app_service",
    }

    ssh_access = Column(Text)
    monitoring = Column(Text)
    # many-to-many relationship
    recommended_apps = relationship(
        "RecommendationAppService",
        secondary="app_service_recommendation",
        back_populates="app_services",
    )

    @property
    def average_rating(self):
        result = (
            db.session.query(func.avg(Score.rating)).filter(Score.service_id == self.id).scalar()
        )
        return round(result, 2) if result is not None else 0.0

    def __repr__(self):
        return f"AppService: {self.name} "
