# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.cart_line_models import CartLine
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_cart_line_display_columns = [
    "id",
    "cart_id",
    "service_id",
    "amount",
    "duration_month",
    "start_date",
    "service",
    "cart",
]


class CartLineModelApi(ModelRestApi):
    resource_name = "CartLine"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(CartLine)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = _cart_line_display_columns
    list_columns = _cart_line_display_columns
    edit_columns = _cart_line_display_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(CartLineModelApi)
