# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_apps.models.nextcloud_subscription_model import (
    NextCloudSubscriptionAppService,
)


class NextCloudAppServiceSubscriptionView(ModelView):
    datamodel = SQLAInterface(NextCloudSubscriptionAppService)

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
    NextCloudAppServiceSubscriptionView,
    "NextCloud  Subscriptions ",
    icon="fa-cogs",
    category="Applications",
)
