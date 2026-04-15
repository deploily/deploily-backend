# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.s3_subscription_model import S3SubscriptionService


class S3SubscriptionServiceView(ModelView):
    datamodel = SQLAInterface(S3SubscriptionService)

    list_columns = [
        "id",
        "created_by",
        "byor",
        "start_date",
        "end_date",
        "is_expired",
        "status",
        "is_upgrade",
        "is_renew",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    S3SubscriptionServiceView,
    "Resource S3 Subscriptions",
    icon="fa-shopping-bag",
    category="Subscriptions",
)
