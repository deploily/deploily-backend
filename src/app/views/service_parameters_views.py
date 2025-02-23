# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app import db
from app.models.parameters_models import Parameter


class ParametersModelView(ModelView):
    route_base = "/admin/parameters"
    datamodel = SQLAInterface(Parameter)
    list_columns = ["id", "name","type", "service"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ParametersModelView,
    "Parameters",
    icon="fa-solid fa-cogs",
    category="Service",
)
