# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.service_plan_models import ServicePlan

_logger = logging.getLogger(__name__)

_service_plan_value_display_columns = [
    "id",
    "price",
    "service_id",
    "service",
    "subscription_category",
    "plan",
    "options",
    "is_custom",
]


class ServicePlanModelApi(ModelRestApi):
    resource_name = "service-plan"
    base_order = ("price", "asc")
    datamodel = SQLAInterface(ServicePlan)
    add_columns = _service_plan_value_display_columns
    list_columns = _service_plan_value_display_columns
    show_columns = _service_plan_value_display_columns
    edit_columns = _service_plan_value_display_columns


appbuilder.add_api(ServicePlanModelApi)
