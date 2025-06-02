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
        "contact_number",
        "mail_support",
        "mail_sales",
        "mail_partnership",
        "phone_sales",
        "phone_partnership",
    ]


appbuilder.add_view(
    ProvidersRessourceServiceView,
    "Ressource Providers",
    icon="fa-users",
    category="Master",
)
