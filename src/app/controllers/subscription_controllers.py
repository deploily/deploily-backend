# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.subscription_models import Subscription
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)
_subscribe_display_columns = [
    "id",
    "start_date",
    "total_amount",
    "price",
    "duration_month",
    "name",
    "status",
    "service_plan",
    "service_details",
    "api_key",
    "service_plan_id",
]


class SubscriptionModelApi(ModelRestApi):
    resource_name = "subscription"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Subscription)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = _subscribe_display_columns
    list_columns = _subscribe_display_columns
    show_columns = _subscribe_display_columns
    edit_columns = _subscribe_display_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(SubscriptionModelApi)
