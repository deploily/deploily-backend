# -*- coding: utf-8 -*-

import logging
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app.models.profile_models import Profile
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_profile_display_columns = [
    "id",
    "name",
    "user_id",
    "user",
    "phone",
    "company_name",
    "company_registration_number"
]


class ProfileModelApi(ModelRestApi):
    resource_name = "profile"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Profile)
    add_columns = _profile_display_columns
    list_columns = _profile_display_columns
    show_columns = _profile_display_columns
    edit_columns = _profile_display_columns


appbuilder.add_api(ProfileModelApi)
