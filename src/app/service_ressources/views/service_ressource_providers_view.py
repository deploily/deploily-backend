# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.services_ressources_providers_model import (
    ProvidersRessourceService,
)


class ProvidersRessourceServiceView(ModelView):
    datamodel = SQLAInterface(ProvidersRessourceService)

    list_columns = [
        "name",
        "logo",
        "short_description",
        "contact_number",
        "website",
        "facebook_page",
        "instagram_page",
        "linkedin_page",
        "extra_info",
        "ressource_service",
        "affiliations",
        "mail_support",
        "mail_sales",
        "mail_partnership",
        "phone_support",
        "phone_sailes",
        "phone_partnership",
    ]


appbuilder.add_view(
    ProvidersRessourceServiceView,
    "ProvidersRessource",
    icon="fa-users",
    category="Service",
)
