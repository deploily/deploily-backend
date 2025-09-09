# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_apps.models.hi_events_subscription_model import (
    HiEventSubscriptionAppService,
)


class HiEventsAppServiceSubscriptionView(ModelView):
    datamodel = SQLAInterface(HiEventSubscriptionAppService)

    list_columns = [
        "id",
        "created_by",
        "price",
        "total_amount",
        "status",
        "is_expired",
        "start_date",
        "duration_month",
        "is_upgrade",
        "is_renew",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    HiEventsAppServiceSubscriptionView,
    "Hi Events  Subscriptions ",
    icon="fa-cogs",
    category="Applications",
)
