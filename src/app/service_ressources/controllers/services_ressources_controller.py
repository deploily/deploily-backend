# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.controllers.service_controllers import ServiceModelApi
from app.service_ressources.models.services_ressources_model import RessourceService

api_columns = [
    "ressource_field",
    "provider",
]


class RessourcesServiceModelApi(ServiceModelApi):
    resource_name = "ressource_service"
    datamodel = SQLAInterface(RessourceService)

    add_columns = ServiceModelApi.add_columns + api_columns
    list_columns = ServiceModelApi.list_columns + api_columns
    show_columns = ServiceModelApi.show_columns + api_columns
    edit_columns = ServiceModelApi.edit_columns + api_columns


appbuilder.add_api(RessourcesServiceModelApi)
