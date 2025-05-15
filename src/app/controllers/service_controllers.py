# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.service_models import Service
from config import DB_LANGUAGES

_logger = logging.getLogger(__name__)

_service_value_display_columns = [
    "id",
    "name",
    "description",
    *[f"description_{lang}" for lang in DB_LANGUAGES if lang != 'en'],
    "documentation_url",
    "unit_price",
    "service_url",
    "image_service",
    "short_description",
    *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != 'en'],
    "specifications",
    *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != 'en'],
    "is_in_favorite",
    "api_playground_url",
]


class ServiceModelApi(ModelRestApi):
    resource_name = "service"
    datamodel = SQLAInterface(Service)
    add_columns = _service_value_display_columns
    list_columns = _service_value_display_columns
    show_columns = _service_value_display_columns
    edit_columns = _service_value_display_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(ServiceModelApi)
