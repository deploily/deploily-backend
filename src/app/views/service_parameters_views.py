# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app import db
from app.models.service_parameters_models import ServiceParameters

class ServiceParametersModelView(ModelView):
    route_base = "/admin/ServiceParameters"
    datamodel = SQLAInterface(ServiceParameters)
    list_columns = ["id", "name", "service"]
    base_order = ("id", "desc")

    add_columns = ["name", "service"]
    edit_columns = ["name", "service"]
    show_columns = ["id", "name", "service"]

db.create_all()
appbuilder.add_view(
    ServiceParametersModelView,
    "ServiceParameters",
    icon="fa-solid fa-cogs",
    category="Service",
)