import logging

from app.service_api.models.api_service_subscription_model import ApiServiceSubscription

_logger = logging.getLogger(__name__)
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, Type, TypeVar


@dataclass
class ApiSubscriptionRequest:
    """Data class for subscription request validation"""

    profile_id: int
    service_plan_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None
    phone: Optional[str] = None


T = TypeVar("T")


class ApiSubscriptionService:

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
            ApiSubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
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
                phone=data.get("phone"),
                # service_plan_selected_id=int(data["service_plan_selected_id"]),
                total_amount=float(data.get("total_amount", 0)),
                duration=int(data["duration"]),
                payment_method=data["payment_method"],
                client_confirm_url=data.get("client_confirm_url"),
                client_fail_url=data.get("client_fail_url"),
                captcha_token=data.get("captcha_token"),
                **(
                    {"service_plan_selected_id": int(data["service_plan_selected_id"])}
                    if request_type == ApiSubscriptionRequest
                    else {}
                ),
            )
            # ✅ Custom validation: enforce duration > 3

            return True, "", request_data
        except (ValueError, TypeError) as e:
            return False, f"Invalid data format: {str(e)}", None

    # Convenience methods for specific validation
    def validate_api_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[ApiSubscriptionRequest]]:
        """Validate new subscription request"""
        return self.validate_request_data(data, ApiSubscriptionRequest)

    def validate_old_api_subscription(self, old_subscription_id: int):
        old_subscription = (
            self.db.query(ApiServiceSubscription).filter_by(id=old_subscription_id).first()
        )
        if not old_subscription:
            return False, "Old Subscription not found", None
        return True, "", old_subscription

    def create_api_subscription(
        self,
        plan,
        duration: int,
        total_amount: float,
        price: float,
        profile_id: int,
        status: str,
        api_key: str,
        phone: str,
    ) -> object:
        """Create api subscription record"""
        subscription = ApiServiceSubscription(
            name=plan.plan.name,
            start_date=datetime.now(),
            total_amount=total_amount,
            price=price,
            service_plan_id=plan.id,
            duration_month=duration,
            status=status,
            payment_status="paid" if status == "active" else "unpaid",
            profile_id=profile_id,
            api_key=api_key,
            phone=phone,
        )

        self.db.add(subscription)
        self.db.flush()
        self.db.commit()
        return subscription
