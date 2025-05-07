# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_cicd.models.cicd_services_model import CicdService


class CicdServiceView(ModelView):
    datamodel = SQLAInterface(CicdService)

    list_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "cicd_field",
    ]
    add_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "cicd_field",
    ]
    edit_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "cicd_field",
    ]
    show_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "cicd_field",
    ]


appbuilder.add_view(
    CicdServiceView,
    "Cicd Services",
    icon="fa-cogs",
    category="Cicd Services",
)
