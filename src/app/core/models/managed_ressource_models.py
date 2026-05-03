# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ManagedRessource(Model):
    __tablename__ = "managed_ressource"

    id = Column(Integer, primary_key=True)
    ip = Column(String(100), nullable=False)  # e.g. "v1.0.0"
    host_name = Column(String(100))
    operating_system = Column(String(100))
    subscriptions = relationship(
        "Subscription", back_populates="managed_ressource", cascade="all, delete-orphan"
    )
    ressource_service_plan = relationship("ServicePlan", back_populates="managed_ressources")
    ressource_service_plan_id = Column(Integer, ForeignKey("service_plan.id"))

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    ressource_type = Column(
        Enum(
            "vps",
            "web_hosting",
            "dns",
            "s3",
            "email",
            name="ressource_type",
        ),
        default="vps",
    )
    dns = Column(String(100))
    gitops_tool = Column(String(100), default="ArgoCD")
    secret_management = Column(String(100))
    backup_automation = Column(String(100), default="k8up")
    monitoring = Column(String(100), default="Kuma")
    kubernetes_distribution = Column(String(100), default="k3s")
    access_user_id = Column(Integer, ForeignKey("ab_user.id"))
    access_user = relationship("User", backref="managed_ressources")
    cd_agent = Column(String(100))
    byor = Column(Boolean, default=False)  # Bring Your Own Ressource

    def __repr__(self):
        return f"{self.ressource_type} - {self.host_name} ({self.ip})"

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

    @property
    def service_details(self):
        sp = self.ressource_service_plan
        if not sp:
            return None

        return {
            "service_name": sp.service.name if sp.service else None,
            "plan": str(sp.plan) if sp.plan else None,
            "provider": sp.provider_info,
            "price": sp.price,
            "subscription_category": sp.subscription_category,
        }

    @property
    def provider_name(self):
        if self.ressource_service_plan and self.ressource_service_plan.provider_info:
            return self.ressource_service_plan.provider_info.get("name", "N/A")
