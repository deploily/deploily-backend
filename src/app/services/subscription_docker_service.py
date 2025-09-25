import logging

_logger = logging.getLogger(__name__)
from dataclasses import dataclass
from typing import Optional, TypeVar


@dataclass
class DockerDeploymentSubscriptionRequest:
    """Data class for subscription request validation"""

    profile_id: int
    # service_plan_selected_id: int
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
