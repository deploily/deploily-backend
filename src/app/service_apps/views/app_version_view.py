# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.service_apps.models.app_version_model import Version


class AppVersionModelView(ModelView):
    route_base = "/admin/app-version"
    datamodel = SQLAInterface(Version)
    list_columns = ["id", "app_services"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    AppVersionModelView,
    "App Version",
    icon="fa-solid fa-cogs",
    category="Operations",
)
