# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.services_ressources_model import RessourceService


class RessourceServiceView(ModelView):
    datamodel = SQLAInterface(RessourceService)

    list_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "ressource_field",
    ]
    add_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "ressource_field",
    ]
    edit_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "ressource_field",
    ]
    show_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "ressource_field",
    ]


appbuilder.add_view(
    RessourceServiceView,
    "Ressources Services",
    icon="fa-cogs",
    category="Ressources Services",
)
