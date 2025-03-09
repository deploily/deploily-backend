# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.utils.utils import get_user
from app import appbuilder
from app.models.service_models import Service

_logger = logging.getLogger(__name__)

_service_value_display_columns = [
    "id",
    "name",
    "description",
    "documentation_url",
    "unit_price",
    "service_url",
    "image_service",
    "short_description",
    "specifications",
    "cart_lines",
    "is_in_favorite",
    "myfavorites",
]


class ServiceModelApi(ModelRestApi):
    resource_name = "service"
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    datamodel = SQLAInterface(Service)
    add_columns = _service_value_display_columns
    list_columns = _service_value_display_columns
    show_columns = _service_value_display_columns
    edit_columns = _service_value_display_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(ServiceModelApi)
