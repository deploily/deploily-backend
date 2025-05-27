# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.services_ressources_providers_model import (
    ProvidersRessourceService,
)

_logger = logging.getLogger(__name__)

_service_ressources_providers_value_display_columns = [
    "id",
    "name",
    "logo",
    "short_description",
    "contact_number",
    "website",
    "facebook_page",
    "instagram_page",
    "linkedin_page",
    "extra_info",
    "mail_support",
    "mail_sales",
    "phone_support",
    "phone_sailes",
    "affiliations",
]


class ProvidersRessourceServiceModelApi(ModelRestApi):
    resource_name = "service-ressource-providers"
    datamodel = SQLAInterface(ProvidersRessourceService)
    add_columns = _service_ressources_providers_value_display_columns
    list_columns = _service_ressources_providers_value_display_columns
    show_columns = _service_ressources_providers_value_display_columns
    edit_columns = _service_ressources_providers_value_display_columns


appbuilder.add_api(ProvidersRessourceServiceModelApi)
