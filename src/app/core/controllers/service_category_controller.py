# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.service_category_models import ServiceCategory

_logger = logging.getLogger(__name__)

_service_category_value_display_columns = [
    "id",
    "name",
    "description",
    "short_description",
    "services",
    "service_details",
]


class ServiceCategoryModelApi(ModelRestApi):
    resource_name = "service-category"
    datamodel = SQLAInterface(ServiceCategory)
    add_columns = _service_category_value_display_columns
    list_columns = _service_category_value_display_columns
    show_columns = _service_category_value_display_columns
    edit_columns = _service_category_value_display_columns


appbuilder.add_api(ServiceCategoryModelApi)
