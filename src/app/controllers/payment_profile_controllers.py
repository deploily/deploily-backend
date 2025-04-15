# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.payment_profile_models import PaymentProfile
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_profile_display_columns = [
    "id",
    "name",
    "last_name",
    "user_id",
    "user",
    "phone",
    "company_name",
    "balance",
    "company_registration_number",
    "balance",
    "is_default_profile",
    "is_company",
    "tax_article",
    "nif",
    "nis",
    "address",
    "city",
    "wilaya",
    "country",
    "postal_code",
]


class PaymentProfileModelApi(ModelRestApi):
    resource_name = "payment-profile"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(PaymentProfile)
    add_columns = _profile_display_columns
    list_columns = _profile_display_columns
    show_columns = _profile_display_columns
    edit_columns = _profile_display_columns
    base_filters = [["user", FilterEqualFunction, get_user]]
    _exclude_columns = ["changed_by", "changed_on", "created_by"]


appbuilder.add_api(PaymentProfileModelApi)
