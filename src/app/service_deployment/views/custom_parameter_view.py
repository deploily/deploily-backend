# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_deployment.models.custom_parameter_model import CustomParameter


class CustomParameterView(ModelView):
    datamodel = SQLAInterface(CustomParameter)

    list_columns = ["name", "description", "value"]
    add_columns = ["name", "description", "value"]
    edit_columns = ["name", "description", "value"]
    show_columns = ["name", "description", "value"]


appbuilder.add_view(
    CustomParameter, "Custom Parameters", icon="fa-cog", category="Service Deployment"
)
