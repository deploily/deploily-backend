# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.service_category_models import ServiceCategory


class ServiceCategoryModelView(ModelView):
    route_base = "/admin/Service-Category"
    datamodel = SQLAInterface(ServiceCategory)
    list_columns = [
        "id",
        "name",
        "short_description",
    ]


db.create_all()
appbuilder.add_view(
    ServiceCategoryModelView,
    "Service Category",
    icon="fa-solid fa-cogs",
    category="Service",
)
