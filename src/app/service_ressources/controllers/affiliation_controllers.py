# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.affiliation_model import Affiliation

_logger = logging.getLogger(__name__)

_affiliation_value_display_columns = [
    "id",
    "total_price",
    "provider",
    "service_plan",
]


class AffiliationModelApi(ModelRestApi):
    resource_name = "affiliation"
    datamodel = SQLAInterface(Affiliation)
    add_columns = _affiliation_value_display_columns
    list_columns = _affiliation_value_display_columns
    show_columns = _affiliation_value_display_columns
    edit_columns = _affiliation_value_display_columns


appbuilder.add_api(AffiliationModelApi)
