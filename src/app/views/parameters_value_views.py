# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.parameters_value_models import ParameterValue


class ParametersValueModelView(ModelView):
    route_base = "/admin/parametersValue"
    datamodel = SQLAInterface(ParameterValue)
    list_columns = ["id", "value", "parameter", "my_service_id"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ParametersValueModelView,
    "Parameters Value",
    icon="fa-solid fa-sliders",
    category="Service",
)
