# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.filters import FilterEqual
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.subscription_models import Subscription


class SubscriptionModelView(ModelView):
    route_base = "/admin/Subscription"
    datamodel = SQLAInterface(Subscription)
    list_columns = [
        "id",
        "created_by",
        "type",
        "byor",
        "start_date",
        "end_date",
        "is_expired",
        "status",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns
    base_permissions = ["can_list", "can_show", "can_delete"]  # only allow viewing


db.create_all()
appbuilder.add_view(
    SubscriptionModelView,
    "Subscription",
    icon="fa-solid fa-shopping-basket",
    category="Subscriptions",
)


class ActiveSubscriptionModelView(ModelView):
    route_base = "/admin/active-subscription"
    datamodel = SQLAInterface(Subscription)
    list_columns = [
        "id",
        "created_by",
        "type",
        "byor",
        "start_date",
        "end_date",
        "is_expired",
        "status",
    ]
    base_order = ("type", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns
    base_permissions = ["can_list", "can_show", "can_delete"]  # only allow viewing
    base_filters = [["status", FilterEqual, "active"]]


db.create_all()
appbuilder.add_view(
    ActiveSubscriptionModelView,
    "Active Subscriptions",
    icon="fa-solid fa-shopping-basket",
    category="Subscriptions",
)
