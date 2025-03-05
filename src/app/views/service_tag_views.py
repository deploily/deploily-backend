# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.service_tag_models import ServiceTag


class ServiceTagModelView(ModelView):
    route_base = "/admin/service-tag"
    datamodel = SQLAInterface(ServiceTag)
    list_columns = ["id", "name", "color", "service_id"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ServiceTagModelView,
    "ServiceTag",
    icon="fa-solid fa-cogs",
    category="Service",
)
