from flask_appbuilder.api import expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.controllers.service_controllers import ServiceModelApi
from app.service_api.models.api_services_model import ApiService

api_columns = [
    "curl_command",
    "service_url",
    "api_playground_url",
]


class ApiServiceModelApi(ServiceModelApi):
    resource_name = "api_service"
    datamodel = SQLAInterface(ApiService)

    add_columns = ServiceModelApi.add_columns + api_columns
    list_columns = ServiceModelApi.list_columns + api_columns
    show_columns = ServiceModelApi.show_columns + api_columns
    edit_columns = ServiceModelApi.edit_columns + api_columns

    @expose("/custom_endpoint", methods=["GET"])
    def custom_endpoint(self):
        return self.response(200, message="Custom API for ApiService")


appbuilder.add_api(ApiServiceModelApi)
