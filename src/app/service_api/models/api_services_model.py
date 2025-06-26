# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, Text, func
from app.utils.utils import get_user
from app import db
from app.core.models import Service
from app.core.models.rating_models import Score
from app.core.models.subscription_models import Subscription
from app.core.models.service_plan_models import ServicePlan


class ApiService(Service):

    __tablename__ = "api_service"
    id = Column(Integer, ForeignKey("service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "api_service",
    }
    apisix_group_id = Column(String(255), nullable=False)
    curl_command = Column(Text)
    service_url = Column(String(255))
    api_playground_url = Column(String(255))

    @property
    def average_rating(self):
        result = (
            db.session.query(func.avg(Score.rating)).filter(
                Score.service_id == self.id).scalar()
        )
        return round(result, 2) if result is not None else 0.0

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

        return subscription is not None and subscription.is_expired==False

    def __repr__(self):
        return f"{self.name} "
