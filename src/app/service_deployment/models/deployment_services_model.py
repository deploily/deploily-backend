# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Text, func

from app import db
from app.core.models import Service
from app.core.models.rating_models import Score


class DeploymentService(Service):

    __tablename__ = "deployment_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "deployment_service",
    }
    deployment_field = Column(Text)
    sequence = Column(Integer)

    @property
    def average_rating(self):
        result = (
            db.session.query(func.avg(Score.rating)).filter(Score.service_id == self.id).scalar()
        )
        return round(result, 2) if result is not None else 0.0

    def __repr__(self):
        return f"DeploymentService: {self.name} "
