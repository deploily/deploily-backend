import logging

_logger = logging.getLogger(__name__)
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, Type, TypeVar


@dataclass
class OdooSubscriptionRequest:
    """Data class for subscription request validation"""

    profile_id: int
    service_plan_selected_id: int
    ressource_service_plan_selected_id: int
    managed_ressource_id: int

    version_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None


@dataclass
class UpgradeOdooSubscriptionRequest:
    """Data class for upgrade subscription request validation"""

    profile_id: int
    old_subscription_id: int
    service_plan_selected_id: int
    ressource_service_plan_selected_id: int
    managed_ressource_id: int
    version_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None


@dataclass
class RenewOdooSubscriptionRequest:
    """Data class for renew subscription request validation"""

    profile_id: int
    old_subscription_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None


T = TypeVar("T")


class SubscriptionOdooService:

    def __init__(self, db_session, logger):
        self.db = db_session
        self.logger = logger

    def validate_request_data(
        self, data: dict, request_type: Type[T]
    ) -> Tuple[bool, str, Optional[T]]:
        """Generic validation function for both subscription types"""
        if not data:
            return False, "Invalid request data", None

        # Define required fields for each request type
        required_fields_map = {
            OdooSubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
                "version_selected_id",
            ],
            RenewOdooSubscriptionRequest: [
                "profile_id",
                "old_subscription_id",
                "duration",
                "payment_method",
            ],
            UpgradeOdooSubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
                # "ressource_service_plan_selected_id",
                "version_selected_id",
                "old_subscription_id",
            ],
        }

        required_fields = required_fields_map.get(request_type, [])

        for field in required_fields:
            if field not in data:
                return False, f"{field} is required", None

        try:
            # Create instance of the specified request type
            request_data = request_type(
                profile_id=int(data["profile_id"]),
                # service_plan_selected_id=int(data["service_plan_selected_id"]),
                total_amount=float(data.get("total_amount", 0)),
                duration=int(data["duration"]),
                payment_method=data["payment_method"],
                promo_code=data.get("promo_code"),
                client_confirm_url=data.get("client_confirm_url"),
                client_fail_url=data.get("client_fail_url"),
                captcha_token=data.get("captcha_token"),
                **(
                    {"old_subscription_id": int(data["old_subscription_id"])}
                    if request_type == RenewOdooSubscriptionRequest
                    else {}
                ),
                **(
                    {
                        "ressource_service_plan_selected_id": (
                            int(data["ressource_service_plan_selected_id"])
                            if "ressource_service_plan_selected_id" in data
                            and data["ressource_service_plan_selected_id"] is not None
                            else None
                        ),
                        "managed_ressource_id": (
                            int(data["managed_ressource_id"])
                            if "managed_ressource_id" in data
                            and data["managed_ressource_id"] is not None
                            else None
                        ),
                        "version_selected_id": int(data["version_selected_id"]),
                        "service_plan_selected_id": int(data["service_plan_selected_id"]),
                    }
                    if request_type == OdooSubscriptionRequest
                    else {}
                ),
                **(
                    {
                        "ressource_service_plan_selected_id": (
                            int(data["ressource_service_plan_selected_id"])
                            if "ressource_service_plan_selected_id" in data
                            and data["ressource_service_plan_selected_id"] is not None
                            else None
                        ),
                        "managed_ressource_id": (
                            int(data["managed_ressource_id"])
                            if "managed_ressource_id" in data
                            and data["managed_ressource_id"] is not None
                            else None
                        ),
                        "version_selected_id": int(data["version_selected_id"]),
                        "old_subscription_id": int(data["old_subscription_id"]),
                        "service_plan_selected_id": int(data["service_plan_selected_id"]),
                    }
                    if request_type == UpgradeOdooSubscriptionRequest
                    else {}
                ),
            )
            # ✅ Custom validation: enforce duration > 3

            if (
                request_type
                in [
                    OdooSubscriptionRequest,
                    UpgradeOdooSubscriptionRequest,
                    RenewOdooSubscriptionRequest,
                ]
                and request_data.duration < 3
            ):
                return False, "Duration must be greater than 3 months", None

            return True, "", request_data
        except (ValueError, TypeError) as e:
            return False, f"Invalid data format: {str(e)}", None

    # Convenience methods for specific validation
    def validate_odoo_renew_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[RenewOdooSubscriptionRequest]]:
        """Validate renew subscription request"""
        return self.validate_request_data(data, RenewOdooSubscriptionRequest)

    def validate_odoo_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[OdooSubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, OdooSubscriptionRequest)

    def validate_upgrade_odoo_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[UpgradeOdooSubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, UpgradeOdooSubscriptionRequest)

    def validate_old_odoo_subscription(self, old_subscription_id: int):
        from app.service_apps.models.odoo_subscription_model import (
            OdooSubscriptionAppService,
        )

        old_subscription = (
            self.db.query(OdooSubscriptionAppService).filter_by(id=old_subscription_id).first()
        )
        if not old_subscription:
            return False, "Old Subscription not found"
        return True, "", old_subscription

    def create_odoo_subscription(
        self,
        plan,
        duration: int,
        total_amount: float,
        price: float,
        promo_code,
        profile_id: int,
        status: str,
        version_id: int,
        # ressource_service_plan,
        is_upgrade: bool = False,
        is_renew: bool = False,
    ) -> object:
        """Create ttk epay subscription record"""
        from app.service_apps.models.odoo_subscription_model import (
            OdooSubscriptionAppService,
        )

        subscription = OdooSubscriptionAppService(
            name=plan.plan.name,
            start_date=datetime.now(),
            total_amount=total_amount,
            price=price,
            service_plan_id=plan.id,
            duration_month=duration,
            promo_code_id=promo_code.id if promo_code else None,
            status=status,
            payment_status="paid" if status == "active" else "unpaid",
            profile_id=profile_id,
            version_id=version_id,
            # ressource_service_plan_id=ressource_service_plan,
        )
        # if is_upgrade:
        #     subscription.is_upgrade = True
        # if is_renew:
        #     subscription.is_renew = True

        self.db.add(subscription)
        self.db.flush()
        return subscription
