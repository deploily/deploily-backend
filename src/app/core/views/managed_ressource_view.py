# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.managed_ressource_model import ManagedRessource


class ManagedRessourcelView(ModelView):
    route_base = "/admin/managed_ressource"
    datamodel = SQLAInterface(ManagedRessource)
    list_columns = ["id", "ip", "hotst_name", "operator_system"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ManagedRessourcelView,
    "Managed Ressources",
    icon="fa-solid fa-cogs",
    category="Operations",
)
