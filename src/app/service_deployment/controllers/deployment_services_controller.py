# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.controllers.service_controllers import ServiceModelApi
from app.service_deployment.models.deployment_services_model import DeploymentService

api_columns = ["deployment_field", "average_rating"]


class DeploymentServiceModelApi(ServiceModelApi):
    resource_name = "deployment-service"
    datamodel = SQLAInterface(DeploymentService)

    add_columns = ServiceModelApi.add_columns + api_columns
    list_columns = ServiceModelApi.list_columns + api_columns
    show_columns = ServiceModelApi.show_columns + api_columns
    edit_columns = ServiceModelApi.edit_columns + api_columns


appbuilder.add_api(DeploymentServiceModelApi)
