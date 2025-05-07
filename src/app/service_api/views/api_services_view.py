from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_api.models.api_services_model import ApiService


class ApiServiceView(ModelView):
    datamodel = SQLAInterface(ApiService)

    list_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        # "additional_place",
    ]
    add_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        # "additional_place",
    ]
    edit_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        # "additional_place",
    ]
    show_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        # "additional_place",
    ]


appbuilder.add_view(
    ApiServiceView,
    "Api Services",
    icon="fa-cogs",
    category="Api Services",
)
