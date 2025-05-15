from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.api_services.api_services import ExtendedService
from config import DB_LANGUAGES

class ExtendedServiceView(ModelView):
    datamodel = SQLAInterface(ExtendedService)

    list_columns = [
        "name",
        "description",
         *[f"description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "short_description",
         *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "specifications",
         *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "additional_place",
    ]
    add_columns = [
        "name",
        "description",
        *[f"description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "short_description",
        *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "specifications",
        *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "additional_place",
    ]
    edit_columns = [
        "name",
        "description",
        *[f"description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "short_description",
        *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "specifications",
        *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "additional_place",
    ]
    show_columns = [
        "name",
        "description",
        *[f"description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "short_description",
        *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "specifications",
        *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != 'en'], 
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "additional_place",
    ]


appbuilder.add_view(
    ExtendedServiceView,
    "Extended Services",
    icon="fa-cogs",
    category="Security",
)
