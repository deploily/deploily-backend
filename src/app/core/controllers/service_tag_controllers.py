# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.service_tag_models import ServiceTag

_logger = logging.getLogger(__name__)
_service_tag_display_columns = ["id", "name", "color", "services"]


class ServiceTagModelApi(ModelRestApi):
    resource_name = "service-tag"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ServiceTag)
    add_columns = _service_tag_display_columns
    list_columns = _service_tag_display_columns
    edit_columns = _service_tag_display_columns
    _exclude_columns = [
        "created_on",
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(ServiceTagModelApi)
