# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ManagedRessource(Model):
    __tablename__ = "managed_ressource"

    id = Column(Integer, primary_key=True)
    ip = Column(String(100), nullable=False)  # e.g. "v1.0.0"
    host_name = Column(String(100))
    operator_system = Column(String(100))
    subscriptions = relationship(
        "Subscription", back_populates="managed_ressource", cascade="all, delete-orphan"
    )
    ressource_service_plan = relationship("ServicePlan", back_populates="managed_ressources")
    ressource_service_plan_id = Column(Integer, ForeignKey("service_plan.id"))

    def __repr__(self):
        return f"{self.host_name} ({self.ip})"

    from datetime import datetime, timedelta

    @property
    def time_remaining(self):
        """Return only the number of full months remaining for the first subscription."""
        if not self.subscriptions:
            return 0

        # ✅ Take the first (earliest) subscription
        first_subscription = min(self.subscriptions, key=lambda s: s.start_date)

        start_date = first_subscription.start_date
        duration_months = first_subscription.duration_month or 0

        # Compute end date
        end_date = start_date + timedelta(days=30 * duration_months)
        now = datetime.now()

        # Calculate remaining days
        remaining_days = (end_date - now).days

        if remaining_days <= 0:
            return 0  # expired

        # Convert to full months
        remaining_months = remaining_days // 30

        return remaining_months
