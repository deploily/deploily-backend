# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.service_models import Service


class ServiceModelView(ModelView):
    route_base = "/admin/Service"
    datamodel = SQLAInterface(Service)
    list_columns = [
        "id",
        "name",
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "is_in_favorite",
        "curl_command",
    ]


db.create_all()
appbuilder.add_view(
    ServiceModelView,
    "Service",
    icon="fa-solid fa-cogs",
    category="Service",
)
