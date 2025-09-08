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






# 📖 STEP 4: Create New Service of App

**Path**:  `app/services/subscription_app_name_service.py`

---

## ✅ Instructions

1. Copy any existing service file from `app/services/`.
2. Rename the copied file with your app’s name.  
3. Inside the file:  
- Rename the **class** with your app’s name.  
- Rename the **functions** with your app’s name.  
- Update the **model import** to point to your new subscription model.  

---

## ✅ Example

```python
def validate_old_new_myapp_subscription(self, old_subscription_id: int):
 from app.service_apps.models.myapp_subscription_model import (
     MyAppSubscriptionAppService,
 )

 old_subscription = (
     self.db.query(MyAppSubscriptionAppService).filter_by(id=old_subscription_id).first()
 )
 if not old_subscription:
     return False, "Old Subscription not found"
 return True, "", old_subscription

```




## ✅ STEP 5: Create Subscribe/Upgrade/Renew Controller

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
        # you sould update only this 
            subscription_new_app_service = SubscriptionNewAppService(db.session, _logger)
            # Validate request data
            data = request.get_json(silent=True)
            is_valid, error_msg, request_data = (
                subscription_odoo_service.validate_new_app_subscription_request(data)
            )
            if not is_valid:
                return self.response_400(message=error_msg)


            subscription = subscription_new_app_service.create_new_app_subscription(
                plan=subscription_json["plan"],
                duration=subscription_json["duration"],
                total_amount=subscription_json["total_amount"],
                price=subscription_json["price"],
                promo_code=subscription_json["promo_code"],
                profile_id=subscription_json["profile"].id,
                status=subscription_status,
                version_id=subscription_json["version_id"],
            )

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
