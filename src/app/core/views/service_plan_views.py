# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.service_plan_models import ServicePlan


class ServicePlanModelView(ModelView):
    route_base = "/admin/service-plan"
    datamodel = SQLAInterface(ServicePlan)
    list_columns = [
        "id",
        "service",
        "plan",
        "price",
        "subscription_category",
        "is_custom",
    ]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ServicePlanModelView,
    "Service Plan",
    icon="fa-solid fa-sliders",
    category="Master",
)
