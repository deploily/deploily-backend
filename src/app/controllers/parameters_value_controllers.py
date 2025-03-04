# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.parameters_value_models import ParameterValue
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_parameters_value_display_columns = [
    "id",
    "name",
    "value",
    "parameter_id",
    "parameter",
    "cart_line_id",
]


class ParameterValueModelApi(ModelRestApi):
    resource_name = "parameter-value"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ParameterValue)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = _parameters_value_display_columns
    list_columns = _parameters_value_display_columns
    edit_columns = _parameters_value_display_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(ParameterValueModelApi)
