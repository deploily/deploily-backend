# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.payment_profile_models import PaymentProfile

_logger = logging.getLogger(__name__)

_profile_display_columns = [
    "id",
    "name",
    "user_id",
    "user",
    "phone",
    "company_name",
    "balance",
    "company_registration_number",
]


class PaymentProfileModelApi(ModelRestApi):
    resource_name = "payment-profile"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(PaymentProfile)
    add_columns = _profile_display_columns
    list_columns = _profile_display_columns
    show_columns = _profile_display_columns
    edit_columns = _profile_display_columns


appbuilder.add_api(PaymentProfileModelApi)
