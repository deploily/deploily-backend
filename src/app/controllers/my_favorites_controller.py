# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app.models.my_favorites_models import MyFavorites
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_support_ticket_display_columns = [
    "id",
    "service_id",
    "created_on",
    "created_by.id",
]


class MyFavoritesModelApi(ModelRestApi):
    resource_name = "MyFavorites"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(MyFavorites)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = _support_ticket_display_columns
    list_columns = ["id", "service", "created_on", "created_by.id"]
    edit_columns = _support_ticket_display_columns
    _exclude_columns = [
        "changed_by",
        "changed_on",
    ]


appbuilder.add_api(MyFavoritesModelApi)
