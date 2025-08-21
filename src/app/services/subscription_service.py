import logging
import os

import requests
from dateutil.relativedelta import relativedelta
from flask import current_app, render_template

from app.core.models import (
    ManagedRessource,
    Payment,
    PaymentProfile,
    PromoCode,
    ServicePlan,
    Subscription,
)
from app.core.models.mail_models import Mail
from app.service_api.models.api_service_subscription_model import ApiServiceSubscription
from app.services.payment_service import PaymentService

_logger = logging.getLogger(__name__)
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple, Type, TypeVar

import requests
from dateutil.relativedelta import relativedelta
from slugify import slugify


@dataclass
class SubscriptionRequest:
    """Data class for subscription request validation"""

    profile_id: int
    service_plan_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None


@dataclass
class TtkEpaySubscriptionRequest:
    """Data class for subscription request validation"""

    profile_id: int
    service_plan_selected_id: int
    ressource_service_plan_selected_id: int
    version_selected_id: int
    managed_ressource_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None


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
class SupabaseSubscriptionRequest:
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
class UpgradeSupabaseSubscriptionRequest:
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
class UpgradeSubscriptionRequest:
    """Data class for upgrade subscription request validation"""

    profile_id: int
    old_subscription_id: int
    service_plan_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None


@dataclass
class UpgradeTtkEpaySubscriptionRequest:
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
class RenewSubscriptionRequest:
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


@dataclass
class RenewTtkEpaySubscriptionRequest:
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


@dataclass
class RenewSupabaseSubscriptionRequest:
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


class SubscriptionService:

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
            SubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
            ],
            TtkEpaySubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
                "version_selected_id",
            ],
            OdooSubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
                "version_selected_id",
            ],
            SupabaseSubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
                "version_selected_id",
            ],
            UpgradeSubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
                "old_subscription_id",
            ],
            RenewSubscriptionRequest: [
                "profile_id",
                "old_subscription_id",
                "duration",
                "payment_method",
            ],
            RenewTtkEpaySubscriptionRequest: [
                "profile_id",
                "old_subscription_id",
                "duration",
                "payment_method",
            ],
            RenewOdooSubscriptionRequest: [
                "profile_id",
                "old_subscription_id",
                "duration",
                "payment_method",
            ],
            RenewOdooSubscriptionRequest: [
                "profile_id",
                "old_subscription_id",
                "duration",
                "payment_method",
            ],
            UpgradeTtkEpaySubscriptionRequest: [
                "profile_id",
                "service_plan_selected_id",
                "duration",
                "payment_method",
                # "ressource_service_plan_selected_id",
                "version_selected_id",
                "old_subscription_id",
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
            UpgradeSupabaseSubscriptionRequest: [
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
                    {
                        "old_subscription_id": int(data["old_subscription_id"]),
                        "service_plan_selected_id": int(data["service_plan_selected_id"]),
                    }
                    if request_type == UpgradeSubscriptionRequest
                    else {}
                ),
                **(
                    {"old_subscription_id": int(data["old_subscription_id"])}
                    if request_type == RenewSubscriptionRequest
                    else {}
                ),
                **(
                    {"old_subscription_id": int(data["old_subscription_id"])}
                    if request_type == RenewTtkEpaySubscriptionRequest
                    else {}
                ),
                **(
                    {"old_subscription_id": int(data["old_subscription_id"])}
                    if request_type == RenewOdooSubscriptionRequest
                    else {}
                ),
                **(
                    {"old_subscription_id": int(data["old_subscription_id"])}
                    if request_type == RenewSupabaseSubscriptionRequest
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
                    if request_type == TtkEpaySubscriptionRequest
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
                        "service_plan_selected_id": int(data["service_plan_selected_id"]),
                    }
                    if request_type == SupabaseSubscriptionRequest
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
                    if request_type == UpgradeTtkEpaySubscriptionRequest
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
                    if request_type == UpgradeSupabaseSubscriptionRequest
                    else {}
                ),
                **(
                    {"service_plan_selected_id": int(data["service_plan_selected_id"])}
                    if request_type == SubscriptionRequest
                    else {}
                ),
            )
            # ✅ Custom validation: enforce duration > 3

            if (
                request_type
                in [
                    TtkEpaySubscriptionRequest,
                    OdooSubscriptionRequest,
                    SupabaseSubscriptionRequest,
                    UpgradeSupabaseSubscriptionRequest,
                    UpgradeOdooSubscriptionRequest,
                    UpgradeTtkEpaySubscriptionRequest,
                    RenewSupabaseSubscriptionRequest,
                    RenewOdooSubscriptionRequest,
                    RenewTtkEpaySubscriptionRequest,
                ]
                and request_data.duration < 3
            ):
                return False, "Duration must be greater than 3 months", None

            return True, "", request_data
        except (ValueError, TypeError) as e:
            return False, f"Invalid data format: {str(e)}", None

    # Convenience methods for specific validation
    def validate_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[SubscriptionRequest]]:
        """Validate new subscription request"""
        return self.validate_request_data(data, SubscriptionRequest)

    def validate_upgrade_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[UpgradeSubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, UpgradeSubscriptionRequest)

    def validate_renew_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[RenewSubscriptionRequest]]:
        """Validate renew subscription request"""
        return self.validate_request_data(data, RenewSubscriptionRequest)

    def validate_ttk_epay_renew_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[RenewTtkEpaySubscriptionRequest]]:
        """Validate renew subscription request"""
        return self.validate_request_data(data, RenewTtkEpaySubscriptionRequest)

    def validate_odoo_renew_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[RenewOdooSubscriptionRequest]]:
        """Validate renew subscription request"""
        return self.validate_request_data(data, RenewOdooSubscriptionRequest)

    def validate_supabase_renew_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[RenewSupabaseSubscriptionRequest]]:
        """Validate renew subscription request"""
        return self.validate_request_data(data, RenewSupabaseSubscriptionRequest)

    def validate_ttk_epay_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[TtkEpaySubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, TtkEpaySubscriptionRequest)

    def validate_odoo_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[OdooSubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, OdooSubscriptionRequest)

    def validate_supabase_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[SupabaseSubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, SupabaseSubscriptionRequest)

    def validate_upgrade_odoo_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[UpgradeOdooSubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, UpgradeOdooSubscriptionRequest)

    def validate_upgrade_supabase_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[UpgradeSupabaseSubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, UpgradeSupabaseSubscriptionRequest)

    def validate_upgrade_ttk_epay_subscription_request(
        self, data: dict
    ) -> Tuple[bool, str, Optional[UpgradeTtkEpaySubscriptionRequest]]:
        """Validate upgrade subscription request"""
        return self.validate_request_data(data, UpgradeTtkEpaySubscriptionRequest)

    def validate_profile(self, user, profile_id: int) -> Tuple[bool, str, Optional[object]]:
        """Validate user profile"""
        profile = self.db.query(PaymentProfile).filter_by(created_by=user, id=profile_id).first()

        if not profile:
            return False, "PaymentProfile not found", None

        if profile.balance is None:
            return False, "Insufficient balance", None

        return True, "", profile

    def validate_service_plan(self, plan_id: int, profile) -> Tuple[bool, str, Optional[object]]:
        """Validate service plan eligibility"""
        plan = self.db.query(ServicePlan).filter_by(id=plan_id).first()

        if not plan:
            return False, "Service Plan not found", None

        if profile.profile_type == "default" and plan.service and not plan.service.is_eligible:
            return False, "This service plan is not eligible for subscription", None

        return True, "", plan

    def validate_ressource_service_plan(
        self, ressource_service_plan_id: int
    ) -> Tuple[bool, str, Optional[object]]:
        """Validate ressource service plan"""
        ressource_service_plan = (
            self.db.query(ServicePlan).filter_by(id=ressource_service_plan_id).first()
        )

        if not ressource_service_plan:
            return False, "Ressource Service Plan not found", None

        return True, "", ressource_service_plan

    def validate_managed_ressource(
        self, managed_ressource_id: int
    ) -> Tuple[bool, str, Optional[object]]:
        """Validate managed ressource"""
        print(
            f"#######################Validating managed ressource with ID: {managed_ressource_id}"
        )

        managed_ressource = (
            self.db.query(ManagedRessource).filter_by(id=managed_ressource_id).first()
        )

        if not managed_ressource:
            return False, "managed_ressource not found", None

        return True, "", managed_ressource

    def validate_version(self, version_id: int) -> Tuple[bool, str, Optional[object]]:
        """Validate version"""
        from app.service_apps.models.app_version_model import Version

        version = self.db.query(Version).filter_by(id=version_id).first()
        if not version:
            return self.response_400(message="Version not found")

        return True, "", version

    def validate_promo_code(
        self, promo_code_str: str, total_amount: float
    ) -> Tuple[Optional[object], float]:
        """Validate and apply promo code"""
        if not promo_code_str:
            return None, 0

        promo_code = self.db.query(PromoCode).filter_by(code=promo_code_str, active=True).first()

        if promo_code and promo_code.is_valid:
            discount_amount = (total_amount * promo_code.rate) / 100
            return promo_code, discount_amount

        return None, 0

    def validate_old_subscription(self, old_subscription_id: int):
        old_subscription = (
            self.db.query(ApiServiceSubscription).filter_by(id=old_subscription_id).first()
        )
        if not old_subscription:
            return False, "Old Subscription not found", None
        return True, "", old_subscription

    def validate_old_ttk_epay_subscription(self, old_subscription_id: int):
        from app.service_apps.models.ttk_epay_subscription_model import (
            TtkEpaySubscriptionAppService,
        )

        old_subscription = (
            self.db.query(TtkEpaySubscriptionAppService).filter_by(id=old_subscription_id).first()
        )
        if not old_subscription:
            return False, "Old Subscription not found"
        return True, "", old_subscription

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

    def validate_old_supabase_subscription(self, old_subscription_id: int):
        from app.service_apps.models.supabase_subscription_model import (
            SupabaseSubscriptionAppService,
        )

        old_subscription = (
            self.db.query(SupabaseSubscriptionAppService).filter_by(id=old_subscription_id).first()
        )
        if not old_subscription:
            return False, "Old Subscription not found"
        return True, "", old_subscription

    def verify_captcha(self, captcha_token: str) -> Tuple[bool, str]:
        """Verify Google reCAPTCHA token"""
        if not captcha_token:
            return False, "Missing CAPTCHA token"

        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {
            "secret": current_app.config["CAPTCHA_SECRET_KEY"],
            "response": captcha_token,
        }

        try:
            response = requests.post(verify_url, data=payload, timeout=10)
            result = response.json()

            if not result.get("success"):
                return False, "CAPTCHA verification failed"

            return True, ""
        except Exception as e:
            self.logger.error(f"Failed to contact reCAPTCHA: {e}", exc_info=True)
            return False, "CAPTCHA verification error"

    def create_api_subscription(
        self,
        plan,
        duration: int,
        total_amount: float,
        price: float,
        promo_code,
        profile_id: int,
        status: str,
        api_key: str,
        is_upgrade: bool = False,
        is_renew: bool = False,
    ) -> object:
        """Create api subscription record"""
        subscription = ApiServiceSubscription(
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
            api_key=api_key,
        )
        # if is_upgrade:
        #     subscription.is_upgrade = True
        # if is_renew:
        #     subscription.is_renew = True

        self.db.add(subscription)
        self.db.flush()
        return subscription

    def create_ttk_epay_subscription(
        self,
        plan,
        duration: int,
        total_amount: float,
        price: float,
        promo_code,
        profile_id: int,
        status: str,
        version_id: int,
        # managed_ressource:int,
        ttk_epay_api_secret_key: str,
        ttk_epay_client_site_url: str,
        ttk_epay_satim_currency: str,
        ttk_epay_mvc_satim_server_url: str,
        ttk_epay_mvc_satim_fail_url: str,
        ttk_epay_mvc_satim_confirm_url: str,
        # ressource_service_plan,
        is_upgrade: bool = False,
        is_renew: bool = False,
    ) -> object:
        """Create ttk epay subscription record"""
        from app.service_apps.models.ttk_epay_subscription_model import (
            TtkEpaySubscriptionAppService,
        )

        subscription = TtkEpaySubscriptionAppService(
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
            # managed_ressource=managed_ressource.id,
            ttk_epay_api_secret_key=ttk_epay_api_secret_key,
            ttk_epay_client_site_url=ttk_epay_client_site_url,
            ttk_epay_satim_currency=ttk_epay_satim_currency,
            ttk_epay_mvc_satim_server_url=ttk_epay_mvc_satim_server_url,
            ttk_epay_mvc_satim_fail_url=ttk_epay_mvc_satim_fail_url,
            ttk_epay_mvc_satim_confirm_url=ttk_epay_mvc_satim_confirm_url,
        )
        # if is_upgrade:
        #     subscription.is_upgrade = True
        # if is_renew:
        #     subscription.is_renew = True

        self.db.add(subscription)
        self.db.flush()
        return subscription

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

    def create_supabase_subscription(
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
        """Create supabase subscription record"""
        from app.service_apps.models.supabase_subscription_model import (
            SupabaseSubscriptionAppService,
        )

        subscription = SupabaseSubscriptionAppService(
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

    def create_payment(
        self, price: float, payment_method: str, subscription_id: int, profile_id: int
    ) -> object:
        """Create payment record"""
        payment = Payment(
            amount=price,
            payment_method=payment_method,
            subscription_id=subscription_id,
            profile_id=profile_id,
            status="pending",
        )

        self.db.add(payment)
        self.db.flush()
        return payment

    def process_payment(
        self, invoice, total_amount: float, is_mvc_call, client_confirm_url, client_fail_url
    ) -> Tuple[bool, str, dict]:
        """Process payment through external service"""
        # payment.order_id = "PAY" + str(payment.id)
        # self.db.commit()

        try:
            payment_service = PaymentService()
            payment_response = payment_service.post_payement(
                invoice.id, total_amount, is_mvc_call, client_confirm_url, client_fail_url
            )[0]

            # Parse response if it's a string
            if isinstance(payment_response, str):
                try:
                    payment_response = json.loads(payment_response)
                except json.JSONDecodeError:
                    return False, "Invalid payment service response format", {}

            if not isinstance(payment_response, dict):
                return False, "Invalid payment service response", {}

            if "ERROR_CODE" in payment_response and payment_response["ERROR_CODE"] != "0":
                error_msg = payment_response.get("ERROR_MESSAGE", "Unknown error")
                return False, f"Payment failed: {error_msg}", {}

            # Update payment with external order ID
            invoice.satim_order_id = payment_response.get("ORDER_ID")
            self.db.commit()

            return True, "", payment_response

        except Exception as e:
            self.logger.error(f"Payment processing error: {e}", exc_info=True)
            return False, "Payment processing failed", {}

    def update_promo_code_usage(self, promo_code, subscription_id: int):
        """Update promo code usage after successful subscription"""
        if not promo_code:
            return

        if promo_code.usage_type == "single_use":
            promo_code.active = False

        promo_code.subscription = subscription_id
        self.db.commit()

    def send_notification_emails(
        self, user, plan, total_amount: float, subscription, payment_method
    ):
        """Send notification emails to admin and user"""
        # Admin notification
        from app.core.celery_tasks.send_mail_task import send_mail

        admin_template = render_template(
            "emails/deploily_subscription.html", user_name=user.username, plan=plan
        )
        bank = agency = address = bank_account_number = None

        if payment_method == "bank_transfer":
            bank = os.getenv("BANK", "")
            agency = os.getenv("AGENCY", "")
            address = os.getenv("ADDRESS", "")
            bank_account_number = os.getenv("BANK_ACCOUNT_NUMBER", "")

        admin_email = Mail(
            title=f"New Subscription Created by {user.username}",
            body=admin_template,
            email_to=current_app.config["NOTIFICATION_EMAIL"],
            email_from=current_app.config["NOTIFICATION_EMAIL"],
            mail_state="outGoing",
        )

        # User notification
        user_template = render_template(
            "emails/user_subscription.html",
            user=user,
            service_name=plan.service.name,
            plan_name=plan.plan.name,
            total_price=total_amount,
            payment_method=payment_method,
            bank=bank,
            agency=agency,
            address=address,
            bank_account_number=bank_account_number,
        )

        user_email = Mail(
            title="Nouvelle souscription à deploily.cloud",
            body=user_template,
            email_to=user.email,
            email_from=current_app.config["NOTIFICATION_EMAIL"],
            mail_state="outGoing",
        )

        # Add to database and send
        self.db.add_all([admin_email, user_email])
        self.db.commit()

        send_mail.delay(admin_email.id)
        send_mail.delay(user_email.id)

        self.logger.info(f"Notification emails sent for subscription {subscription.id}")

    # def update_old_subscription(self, old_subscription,):
    #     """Update old subscrption  after successful Upgrade subscription"""

    #     old_subscription.start_date = datetime.now() - relativedelta(
    #         months=old_subscription.duration_month + 1
    #     )
    #     old_subscription.status = "inactive"
    #     old_subscription.is_upgrade = True

    #     self.db.commit()

    def update_old_subscription(
        self, old_subscription, is_renew: bool = False, is_upgrade: bool = False
    ):
        """Update old subscription after successful upgrade or renewal"""

        # Mark the subscription as expired by shifting the start date far in the past
        old_subscription.start_date = datetime.now() - relativedelta(
            months=old_subscription.duration_month + 1
        )
        # old_subscription.status = "inactive"

        # Set the correct flag
        if is_renew:
            old_subscription.is_renew = True
        if is_upgrade:
            old_subscription.is_upgrade = True

        self.db.commit()

    def create_managed_ressource(self, ressource_service_plan, subscription=None):
        """Create managed ressource record"""
        # todo host_name should be : slug(subscription.profile_id.name)-(subscription.id)
        managed_ressource = ManagedRessource(
            ressource_service_plan_id=ressource_service_plan,
            ip="000.000.000.000",
            host_name=f"{slugify(subscription.profile.name)}-({subscription.id})",
            operator_system="Debian 12",
        )
        self.db.add(managed_ressource)
        self.db.flush()
        return managed_ressource

    def get_or_create_managed_ressource(self, ressource_plan, managed_ressource, subscription):
        """
        Assigns a managed ressource to the subscription.

        """
        _logger.info(f"🛠 Getting or creating managed ressource for subscription {subscription.id}")

        if ressource_plan is None and managed_ressource is None:
            return None

        user_id = subscription.created_by

        # Use provided managed_ressource if available
        if managed_ressource:
            subscription.managed_ressource_id = managed_ressource.id
            self.db.commit()
            _logger.info(f"✅ Used provided managed ressource ID: {managed_ressource.id}")
            return managed_ressource

        existing = (
            self.db.query(ManagedRessource)
            .join(Subscription, Subscription.managed_ressource_id == ManagedRessource.id)
            .filter(
                ManagedRessource.ressource_service_plan_id == ressource_plan.id,
                Subscription.created_by == user_id,
            )
            .first()
        )

        if existing:
            _logger.info(f"🔄 Found existing managed ressource ID: {existing.id}")
            subscription.managed_ressource_id = existing.id
            self.db.commit()
            return existing

        # Create new
        new_managed = self.create_managed_ressource(
            ressource_service_plan=ressource_plan.id, subscription=subscription
        )
        subscription.managed_ressource_id = new_managed.id
        self.db.commit()
        _logger.info(f"🆕 Created new managed ressource ID: {new_managed.id}")
        return new_managed

    # def get_remaining_value(self, old_subscription):
    #     total_price = old_subscription.price
    #     start_date = old_subscription.start_date
    #     duration_month = old_subscription.duration_month

    #     end_date = start_date + relativedelta(months=duration_month)
    #     today = datetime.now()

    #     # Ensure today is not beyond the end date
    #     if today > end_date:
    #         return 0.0

    #     total_days = (end_date - start_date).days
    #     used_days = (today - start_date).days
    #     remaining_days = total_days - used_days

    #     if total_days == 0:
    #         return 0.0

    #     remaining_value = (remaining_days / total_days) * total_price
    #     return round(remaining_value, 2)

    def get_date_diff_in_days(self, date1, date2):
        """
        Returns the number of full days between two dates.
        """
        if isinstance(date1, str):
            date1 = datetime.fromisoformat(date1)
        if isinstance(date2, str):
            date2 = datetime.fromisoformat(date2)

        d1_ms = date1.timestamp() * 1000  # milliseconds since epoch
        d2_ms = date2.timestamp() * 1000

        return (d2_ms - d1_ms) / (1000 * 60 * 60 * 24)  # exact float days

    def get_remaining_value(self, old_subscription):

        total_price = old_subscription.price
        start_date = old_subscription.start_date
        duration_month = old_subscription.duration_month

        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)

        end_date = start_date + relativedelta(months=duration_month)
        today = datetime.now()

        # If subscription expired
        if today >= end_date:
            return 0.0

        # If subscription hasn't started yet
        if today <= start_date:
            return round(total_price)

        remaining_days = self.get_date_diff_in_days(start_date, today)
        total_days = duration_month * 30  # Assuming each month has ~30 days
        remaining_value = ((total_days - remaining_days) * total_price) / total_days

        return round(remaining_value)
