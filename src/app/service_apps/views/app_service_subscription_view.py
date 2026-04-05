# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)


class SubscriptionAppServiceView(ModelView):
    datamodel = SQLAInterface(SubscriptionAppService)

    list_columns = [
        "id",
        "created_by",
        "service_name",
        "byor",
        "start_date",
        "end_date",
        "is_expired",
        "status",
        "application_status",
        "required_restart",
    ]

    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns
    base_permissions = ["can_list", "can_show"]  # only allow viewing


appbuilder.add_view(
    SubscriptionAppServiceView,
    "Application Services Subscriptions",
    icon="fa-shopping-bag",
    category="Subscriptions",
)
