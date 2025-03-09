# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.parameters_models import Parameter

_logger = logging.getLogger(__name__)
_parameter_display_columns = ["id", "name", "type", "service_id"]


class ParametersModelApi(ModelRestApi):
    resource_name = "parameter"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Parameter)
    add_columns = _parameter_display_columns
    list_columns = _parameter_display_columns
    edit_columns = _parameter_display_columns


appbuilder.add_api(ParametersModelApi)
