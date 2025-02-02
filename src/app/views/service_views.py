# -*- coding: utf-8 -*-


# TODO 5


# TODO post_update 
# TODO create Service + Route + Upstream + ...


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app import db
from app.models.service_models import Service


class ServiceModelView(ModelView):
    route_base = "/admin/service"
    datamodel = SQLAInterface(Service)
    list_columns = ["id", "name","order"]
    base_order = ("id", "desc")

    add_columns = ["name","order"]
    edit_columns = ["name","order"]
    show_columns = ["id", "name", "order"]


db.create_all()
appbuilder.add_view(
    ServiceModelView,
    "Service",
    icon="fa-solid fa-cogs",
    category="Service",
)
