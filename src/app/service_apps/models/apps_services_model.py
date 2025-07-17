# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app import db
from app.core.models import Service
from app.core.models.rating_models import Score
from app.core.models.subscription_models import Subscription
from app.utils.utils import get_user


class AppService(Service):
    __tablename__ = "app_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "app_service",
    }

    minimal_cpu = Column(Integer, nullable=False)
    minimal_ram = Column(Integer, nullable=False)
    minimal_disk = Column(Integer, nullable=False)
    # many-to-many relationship
    recommended_apps = relationship(
        "RecommendationAppService",
        secondary="app_service_recommendation",
        back_populates="app_services",
    )

    app_versions = relationship(
        "Version",
        secondary="app_service_version",
        back_populates="app_services",
    )

    @property
    def is_subscribed(self):

        user = get_user()
        if not user.is_authenticated:
            return False
        subscription = (
            db.session.query(Subscription)
            .filter(
                Subscription.service_plan.has(service_id=self.id),
                Subscription.created_by_fk == user.id,
                Subscription.status == "active",
            )
            .first()
        )

        return subscription is not None and subscription.is_expired == False

    @property
    def min_app_price(self):
        prices = [plan.price for plan in self.service_plans if plan.price is not None]
        return min(prices) if prices else None

    @property
    def average_rating(self):
        result = (
            db.session.query(func.avg(Score.rating)).filter(Score.service_id == self.id).scalar()
        )
        return round(result, 2) if result is not None else 0.0

    def __repr__(self):
        return f"AppService: {self.name} "
