# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.contact_us_models import ContactUs

_logger = logging.getLogger(__name__)
_contact_us_display_columns = ["id", "name", "email", "message", "created_on"]


class ContactUSModelApi(ModelRestApi):
    resource_name = "contact-us"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ContactUs)
    add_columns = ["id", "name", "email", "message"]
    list_columns = _contact_us_display_columns
    edit_columns = _contact_us_display_columns
    _exclude_columns = ["changed_by", "changed_on", "created_by.id"]


appbuilder.add_api(ContactUSModelApi)
