# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.payment_models import Payment

_logger = logging.getLogger(__name__)
_payment_display_columns = [
    "id",
    "amount",
    "status",
    "start_date",
    "payment_method",
    "subscription_id",
    "profile_id",
    "subscription",
    "profile",
]


class PaymentModelApi(ModelRestApi):
    resource_name = "payment"
    base_order = ("id", "desc")
    exclude_route_methods = "delete"
    datamodel = SQLAInterface(Payment)
    add_columns = _payment_display_columns
    list_columns = _payment_display_columns
    edit_columns = _payment_display_columns


appbuilder.add_api(PaymentModelApi)
