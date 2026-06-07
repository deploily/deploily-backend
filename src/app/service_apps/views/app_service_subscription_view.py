# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.filters import FilterEqual
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
        "ressource_service_plan",
        "byor",
        "start_date",
        "end_date",
        "total_amount",
        "status",
        "application_status",
        "required_restart",
    ]

    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    SubscriptionAppServiceView,
    "Application Services Subscriptions",
    icon="fa-shopping-bag",
    category="Subscriptions",
)


class TrialSubscriptionModelView(ModelView):
    route_base = "/admin/trial-subscription"
    datamodel = SQLAInterface(SubscriptionAppService)
    list_columns = [
        "id",
        "created_by",
        "type",
        "byor",
        "start_date",
        "end_date",
        "total_amount",
    ]
    base_order = ("start_date", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns
    base_filters = [["is_trial", FilterEqual, True]]


appbuilder.add_view(
    TrialSubscriptionModelView,
    "Trial Subscriptions",
    icon="fa-solid fa-shopping-basket",
    category="Subscriptions",
)
