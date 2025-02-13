import logging
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.parameters_value_models import ParameterValue
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_parameters_value_display_columns = [
    "id",
    "value",
    "parameter_id",
    "cart_line_id"
]


class ParameterValueModelApi(ModelRestApi):
    resource_name = "ParameterValue"
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
