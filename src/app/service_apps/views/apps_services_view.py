# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_apps.models.apps_services_model import AppService


class AppServiceView(ModelView):
    datamodel = SQLAInterface(AppService)

    list_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "apps_field",
    ]
    add_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "apps_field",
    ]
    edit_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "apps_field",
    ]
    show_columns = [
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "apps_field",
    ]


appbuilder.add_view(
    AppServiceView,
    "App Services",
    icon="fa-cogs",
    category="App Services",
)
