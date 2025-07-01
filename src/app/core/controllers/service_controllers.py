# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.service_models import Service

_logger = logging.getLogger(__name__)

_service_value_display_columns = [
    "id",
    "name",
    "description",
    "documentation_url",
    "unit_price",
    "image_service",
    "short_description",
    "specifications",
    "is_in_favorite",
    "service_details",
    "type",
    "medias",
    "is_eligible",
    "service_slug",
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
