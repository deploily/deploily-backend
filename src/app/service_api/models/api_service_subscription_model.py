# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer

from app.core.models import Subscription


class ApiServiceSubscription(Subscription):
    __tablename__ = "subscription_api_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_api_service",
    }

    def to_dict(self):
        return {
            "id": self.id,
            "is_expired": self.is_expired,
            "name": self.name,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "total_amount": self.total_amount,
            "price": self.price,
            "payment_status": self.payment_status,
            "duration_month": self.duration_month,
            "status": self.status,
            "service_plan_id": self.service_plan.id if self.service_plan else None,
            # "service_plan_name": self.service_plan.name if self.service_plan else None,
            "promo_code_id": self.promo_code.id if self.promo_code else None,
            "promo_code_name": self.promo_code.code if self.promo_code else None,
            "api_key": self.api_key,
            "is_encrypted": self.is_encrypted,
            "profile_id": self.profile.id if self.profile else None,
            "profile_name": self.profile.name if hasattr(self.profile, "name") else None,
            "is_upgrade": self.is_upgrade,
            "is_renew": self.is_renew,
            "is_expired": self.is_expired,
        }
