# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.contact_us_models import ContactUs

_logger = logging.getLogger(__name__)

_contact_us_value_display_columns = ["id", "name", "email", "message", "phone", "ressource"]


class ContactUsModelApi(ModelRestApi):
    resource_name = "ressource-category"
    datamodel = SQLAInterface(ContactUs)
    add_columns = _contact_us_value_display_columns
    list_columns = _contact_us_value_display_columns
    show_columns = _contact_us_value_display_columns
    edit_columns = _contact_us_value_display_columns
    exclude_route_methods = ["get", "put", "get_list"]
    search_columns = ["name", "description"]


appbuilder.add_api(ContactUsModelApi)
