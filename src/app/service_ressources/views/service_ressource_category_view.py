# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.service_ressources.models.services_ressources_category_model import (
    ServiceRessouceCategory,
)


class ServiceRessourceCategoryModelView(ModelView):
    route_base = "/admin/ressources-Category"
    datamodel = SQLAInterface(ServiceRessouceCategory)
    list_columns = [
        "id",
        "name",
        "short_description",
    ]


db.create_all()
appbuilder.add_view(
    ServiceRessourceCategoryModelView,
    "Reesource Category",
    icon="fa-solid fa-cogs",
    category="Master",
)
