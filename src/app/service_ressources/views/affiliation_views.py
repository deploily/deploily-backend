# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.affiliation_model import Affiliation


class AffiliationView(ModelView):
    datamodel = SQLAInterface(Affiliation)
    route_base = "/admin/affiliation"

    list_columns = ["total_price", "affiliation_state", "provider", "service_plan", "created_by"]

    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    AffiliationView,
    "Affiliation",
    icon="fa-solid fa-sliders",
    category="Service",
)
