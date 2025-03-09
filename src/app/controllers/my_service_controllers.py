# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app.models.my_service_models import MyService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_cart_line_display_columns = [
    "id",
    "start_date",
    "amount",
    "duration_month",
    "name"
]


class MyServiceModelApi(ModelRestApi):
    resource_name = "my-service"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(MyService)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = _cart_line_display_columns
    list_columns = _cart_line_display_columns
    show_columns = _cart_line_display_columns
    edit_columns = _cart_line_display_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(MyServiceModelApi)
