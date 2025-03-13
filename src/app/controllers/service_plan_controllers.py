# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.utils.utils import get_user
from app import appbuilder
from app.models.service_plan_models import ServicePlan

_logger = logging.getLogger(__name__)

_service_plan_value_display_columns = [
    "id",
    "price",
    "limit",
    "service_id",
    "service",
    "ubscription_category",
    "plan",
    "options"
]


class ServicePlanModelApi(ModelRestApi):
    resource_name = "service-plan"
    datamodel = SQLAInterface(ServicePlan)
    add_columns = _service_plan_value_display_columns
    list_columns = _service_plan_value_display_columns
    show_columns = _service_plan_value_display_columns
    edit_columns = _service_plan_value_display_columns


appbuilder.add_api(ServicePlanModelApi)
