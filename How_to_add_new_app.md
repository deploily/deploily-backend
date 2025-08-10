# 🚀 Add New App to Deploily Backend

This guide describes the **step-by-step process** to integrate a new application (e.g., `MyApp`) into the Deploily subscription management backend.

---

## ✅ STEP 1: Create Subscription Model

📁 **Path**: `app/service_apps/models/myapp_subscription_model.py`

```python
from app.service_apps.models.base_subscription_model import SubscriptionAppService

class MyAppSubscriptionService(SubscriptionAppService):
    """MyApp-specific subscription logic"""
    pass  # Add app-specific fields or methods here if needed
```

---

## ✅ STEP 2: Create Subscription Views

📁 **Path**: `app/service_apps/views/myapp_subscription_view.py`

```python
from app.service_apps.models.myapp_subscription_model import MyAppSubscriptionService
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

class MyAppSubscriptionView(ModelView):
    datamodel = SQLAInterface(MyAppSubscriptionService)

    list_columns = [......]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns

appbuilder.add_view(
    MyAppSubscriptionView,
    "MyApp Subscriptions",
    icon="fa-cogs",
    category="Applications",
)
```

---

## ✅ STEP 3: Create Subscription Controller

📁 **Path**: `app/service_apps/controllers/myapp_subscription_controller.py`

```python
from app.service_apps.models.myapp_subscription_model import MyAppSubscriptionService
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

api_columns = [......]

class MyAppSubscriptionApi(ModelRestApi):
    resource_name = "myapp-subscription"
    datamodel = SQLAInterface(MyAppSubscriptionService)

    add_columns = api_columns
    list_columns = api_columns
    show_columns = api_columns
    edit_columns = api_columns

appbuilder.add_api(MyAppSubscriptionApi)
```

---

## ✅ STEP 4: Create Subscribe/Upgrade/Renew Controller

📁 **Path**: `app/service_apps/controllers/myapp_subscribe_to_plan_subscription_controller.py`

```python
from flask_appbuilder.api import expose
from flask_appbuilder.security.decorators import protect
from flask_jwt_extended import jwt_required
from flask_appbuilder.api import BaseApi
from app.decorators import rison

class MyAppSubscriptionApi(BaseApi):
    resource_name = "myapp-app-service-subscription"

    @expose("/subscribe", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def subscribe_to_plan(self, **kwargs):
        pass

    @expose("/upgrade", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def upgrade_app_subscription(self, **kwargs):
        pass

    @expose("/renew", methods=["POST"])
    @protect()
    @rison()
    @jwt_required()
    def renew_app_subscription(self, **kwargs):
        pass
```
---

## ✅ STEP 5: Add Dataclasses for Request Validation

📁 **Path**: `app/services/subscription_service.py`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MyAppSubscriptionRequest:
    profile_id: int
    service_plan_selected_id: int
    ressource_service_plan_selected_id: int
    version_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None

@dataclass
class UpgradeMyAppSubscriptionRequest:
    profile_id: int
    old_subscription_id: int
    service_plan_selected_id: int
    ressource_service_plan_selected_id: int
    version_selected_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None

@dataclass
class RenewMyAppSubscriptionRequest:
    profile_id: int
    old_subscription_id: int
    total_amount: float
    duration: int
    payment_method: str
    promo_code: Optional[str] = None
    captcha_token: Optional[str] = None
    client_confirm_url: Optional[str] = None
    client_fail_url: Optional[str] = None
```

---

## ✅ STEP 6: Add to `required_fields_map`

Within the `validate_request_data()` method:

```python
required_fields_map = {
    ...
    MyAppSubscriptionRequest: [
        "profile_id",
        "service_plan_selected_id",
        "ressource_service_plan_selected_id",
        "version_selected_id",
        "duration",
        "payment_method",
    ],
    UpgradeMyAppSubscriptionRequest: [
        "profile_id",
        "old_subscription_id",
        "service_plan_selected_id",
        "ressource_service_plan_selected_id",
        "version_selected_id",
        "duration",
        "payment_method",
    ],
    RenewMyAppSubscriptionRequest: [
        "profile_id",
        "old_subscription_id",
        "duration",
        "payment_method",
    ],
}
```

---

## ✅ STEP 7: Add Construction Logic

Inside the `validate_request_data()` method try block:

```python
**(
    {
        "ressource_service_plan_selected_id": int(data["ressource_service_plan_selected_id"]),
        "version_selected_id": int(data["version_selected_id"]),
        "service_plan_selected_id": int(data["service_plan_selected_id"]),
    }
    if request_type == MyAppSubscriptionRequest
    else {}
),
**(
    {
        "ressource_service_plan_selected_id": int(data["ressource_service_plan_selected_id"]),
        "version_selected_id": int(data["version_selected_id"]),
        "old_subscription_id": int(data["old_subscription_id"]),
        "service_plan_selected_id": int(data["service_plan_selected_id"]),
    }
    if request_type == UpgradeMyAppSubscriptionRequest
    else {}
),
**(
    {
        "old_subscription_id": int(data["old_subscription_id"]),
    }
    if request_type == RenewMyAppSubscriptionRequest
    else {}
),
```

---

## ✅ STEP 8: Optional Custom Validation

Still in `validate_request_data()`:

```python
if (
    request_type
    in [
        MyAppSubscriptionRequest,
        UpgradeMyAppSubscriptionRequest,
        RenewMyAppSubscriptionRequest,
    ]
    and request_data.duration < 3
):
    return False, "Duration must be greater than 3 months", None
```

---

## ✅ STEP 9: Add Validation Shortcuts

At the bottom of `SubscriptionService`:

```python
def validate_my_app_subscription_request(
    self, data: dict
) -> Tuple[bool, str, Optional[MyAppSubscriptionRequest]]:
    return self.validate_request_data(data, MyAppSubscriptionRequest)

def validate_my_app_upgrade_request(
    self, data: dict
) -> Tuple[bool, str, Optional[UpgradeMyAppSubscriptionRequest]]:
    return self.validate_request_data(data, UpgradeMyAppSubscriptionRequest)

def validate_my_app_renew_request(
    self, data: dict
) -> Tuple[bool, str, Optional[RenewMyAppSubscriptionRequest]]:
    return self.validate_request_data(data, RenewMyAppSubscriptionRequest)
```

---

## ✅ STEP 10: Create Subscription Logic

Inside `SubscriptionService`:

```python
from datetime import datetime

def create_my_app_subscription(
    self,
    plan,
    duration: int,
    total_amount: float,
    price: float,
    promo_code,
    profile_id: int,
    status: str,
    version_id: int,
    ressource_service_plan,
    is_upgrade: bool = False,
    is_renew: bool = False,
) -> object:
    """Create MyApp subscription record"""
    from app.service_apps.models.myapp_subscription_model import MyAppSubscriptionService

    subscription = MyAppSubscriptionService(
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
        ressource_service_plan_id=ressource_service_plan,
        is_upgrade=is_upgrade,
        is_renew=is_renew,
    )

    self.db.add(subscription)
    self.db.flush()
    return subscription
```