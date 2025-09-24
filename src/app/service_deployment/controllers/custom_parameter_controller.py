# -*- coding: utf-8 -*-

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_deployment.models.custom_parameter_model import CustomParameter

api_columns = ["deployment_field", "average_rating"]

_deployment_service_display_columns = [
    "id",
    "name",
    "description",
    "value",
    "deployment_subscription_id",
]


class CustomParameterModelApi(ModelRestApi):
    resource_name = "custom-parameter"
    datamodel = SQLAInterface(CustomParameter)

    add_columns = _deployment_service_display_columns
    list_columns = _deployment_service_display_columns
    show_columns = _deployment_service_display_columns
    edit_columns = _deployment_service_display_columns


appbuilder.add_api(CustomParameterModelApi)
