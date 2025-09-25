import logging

_logger = logging.getLogger(__name__)
from dataclasses import dataclass
from typing import Optional, TypeVar


@dataclass
class DockerDeploymentSubscriptionRequest:
    """Data class for subscription request validation"""

    profile_id: int
    service_plan_selected_id: int
    # ressource_service_plan_selected_id: int
    # version_selected_id: int
    # managed_ressource_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class UpgradeDockerDeploymentSubscriptionRequest:
    """Data class for upgrade subscription request validation"""

    profile_id: int
    old_subscription_id: int
    service_plan_selected_id: int
    # ressource_service_plan_selected_id: int
    # ! i don't know if we need it
    # managed_ressource_id: int
    # version_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None
    phone: Optional[str] = None


@dataclass
class RenewDockerDeploymentSubscriptionRequest:
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
    phone: Optional[str] = None


T = TypeVar("T")


class SubscriptionDockerDeploymentService:

    def __init__(self, db_session, logger):
        self.db = db_session
        self.logger = logger

    # def validate_request_data(
    #     self, data: dict, request_type: Type[T]
    # ) -> Tuple[bool, str, Optional[T]]:
    #     """Generic validation function for both subscription types"""
    #     if not data:
    #         return False, "Invalid request data", None

    #     # Define required fields for each request type
    #     required_fields_map = {
    #         DockerDeploymentSubscriptionRequest: [
    #             "profile_id",
    #             "service_plan_selected_id",
    #             "duration",
    #             "payment_method",
    #             # "version_selected_id",
    #         ],
    #         UpgradeDockerDeploymentSubscriptionRequest: [
    #             "profile_id",
    #             "old_subscription_id",
    #             "duration",
    #             "payment_method",
    #         ],
    #         RenewDockerDeploymentSubscriptionRequest: [
    #             "profile_id",
    #             "service_plan_selected_id",
    #             "duration",
    #             "payment_method",
    #             # "ressource_service_plan_selected_id",
    #             # "version_selected_id",
    #             "old_subscription_id",
    #         ],
    #     }

    #     required_fields = required_fields_map.get(request_type, [])

    #     for field in required_fields:
    #         if field not in data:
    #             return False, f"{field} is required", None

    #     try:
    #         # Create instance of the specified request type
    #         request_data = request_type(
    #             profile_id=int(data["profile_id"]),
    #             # service_plan_selected_id=int(data["service_plan_selected_id"]),
    #             total_amount=float(data.get("total_amount", 0)),
    #             duration=int(data["duration"]),
    #             phone=data.get("phone"),
    #             payment_method=data["payment_method"],
    #             promo_code=data.get("promo_code"),
    #             client_confirm_url=data.get("client_confirm_url"),
    #             client_fail_url=data.get("client_fail_url"),
    #             captcha_token=data.get("captcha_token"),
    #             **(
    #                 {"old_subscription_id": int(data["old_subscription_id"])}
    #                 if request_type == RenewDockerDeploymentSubscriptionRequest
    #                 else {}
    #             ),
    #             **(
    #                 {
    #                     "ressource_service_plan_selected_id": (
    #                         int(data["ressource_service_plan_selected_id"])
    #                         if "ressource_service_plan_selected_id" in data
    #                         and data["ressource_service_plan_selected_id"] is not None
    #                         else None
    #                     ),
    #                     "managed_ressource_id": (
    #                         int(data["managed_ressource_id"])
    #                         if "managed_ressource_id" in data
    #                         and data["managed_ressource_id"] is not None
    #                         else None
    #                     ),
    #                     "version_selected_id": int(data["version_selected_id"]),
    #                     "service_plan_selected_id": int(
    #                         data["service_plan_selected_id"]
    #                     ),
    #                 }
    #                 if request_type == TtkEpaySubscriptionRequest
    #                 else {}
    #             ),
    #             **(
    #                 {
    #                     "ressource_service_plan_selected_id": (
    #                         int(data["ressource_service_plan_selected_id"])
    #                         if "ressource_service_plan_selected_id" in data
    #                         and data["ressource_service_plan_selected_id"] is not None
    #                         else None
    #                     ),
    #                     "managed_ressource_id": (
    #                         int(data["managed_ressource_id"])
    #                         if "managed_ressource_id" in data
    #                         and data["managed_ressource_id"] is not None
    #                         else None
    #                     ),
    #                     "version_selected_id": int(data["version_selected_id"]),
    #                     "old_subscription_id": int(data["old_subscription_id"]),
    #                     "service_plan_selected_id": int(
    #                         data["service_plan_selected_id"]
    #                     ),
    #                 }
    #                 if request_type == UpgradeTtkEpaySubscriptionRequest
    #                 else {}
    #             ),
    #         )
    #         # ✅ Custom validation: enforce duration > 3

    #         if (
    #             request_type
    #             in [
    #                 TtkEpaySubscriptionRequest,
    #                 UpgradeTtkEpaySubscriptionRequest,
    #                 RenewTtkEpaySubscriptionRequest,
    #             ]
    #             and request_data.duration < 3
    #         ):
    #             return False, "Duration must be greater than 3 months", None

    #         return True, "", request_data
    #     except (ValueError, TypeError) as e:
    #         return False, f"Invalid data format: {str(e)}", None
