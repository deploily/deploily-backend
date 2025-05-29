# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.plan_models import Plan


class PlanModelView(ModelView):
    route_base = "/admin/plan"
    datamodel = SQLAInterface(Plan)
    list_columns = ["id", "name", "description"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    PlanModelView,
    "Plan",
    icon="fa-solid fa-sliders",
    category="Master",
)
