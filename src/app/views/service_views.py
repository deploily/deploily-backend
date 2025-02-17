# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app import db
from app.models.service_models import Service


class ServiceModelView(ModelView):
    route_base = "/admin/Service"
    datamodel = SQLAInterface(Service)
    list_columns = ["id", "name", "parameters", "description", "short_description", "specifications",
                    "documentation_url", "unit_price", "service_url", "image_service"]

db.create_all()
appbuilder.add_view(
    ServiceModelView,
    "Service",
    icon="fa-solid fa-cogs",
    category="Service",
)
