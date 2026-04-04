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
        "phone_partnership",
        "mail_partnership",
        "mail_support",
        "is_published",
    ]


appbuilder.add_view(
    ProvidersRessourceServiceView,
    "Ressource Providers",
    icon="fa-users",
    category="Master",
)
