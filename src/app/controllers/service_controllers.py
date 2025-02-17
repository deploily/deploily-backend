# -*- coding: utf-8 -*-

import logging
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.service_models import Service

_logger = logging.getLogger(__name__)

_service_value_display_columns = [
    "id",
    "name",
    "description",
    "documentation_url",
    "unit_price",
    "service_url",
    "image_service",
    "short_description",
    "specifications"
]


class ServiceModelApi(ModelRestApi):
    resource_name = "service"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Service)
    add_columns = _service_value_display_columns
    list_columns = _service_value_display_columns
    edit_columns = _service_value_display_columns


appbuilder.add_api(ServiceModelApi)
