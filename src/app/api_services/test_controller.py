from flask_appbuilder.api import expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.api_services.api_services import ExtendedService
from app.controllers.service_controllers import ServiceModelApi


class ExtendedServiceModelApi(ServiceModelApi):
    resource_name = "extended_service"
    datamodel = SQLAInterface(ExtendedService)

    add_columns = ServiceModelApi.add_columns + ["additional_place"]
    list_columns = ServiceModelApi.list_columns + ["additional_place"]
    show_columns = ServiceModelApi.show_columns + ["additional_place"]
    edit_columns = ServiceModelApi.edit_columns + ["additional_place"]

    @expose("/custom_endpoint", methods=["GET"])
    def custom_endpoint(self):
        return self.response(200, message="Custom API for ExtendedService")


appbuilder.add_api(ExtendedServiceModelApi)
