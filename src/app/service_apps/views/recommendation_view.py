# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.service_apps.models.recommendation_app_services import RecommendationAppService


class AppRecommendationModelView(ModelView):
    route_base = "/admin/app-recommendation"
    datamodel = SQLAInterface(RecommendationAppService)
    list_columns = ["id", "app_services"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    AppRecommendationModelView,
    "App Recommendation",
    icon="fa-solid fa-cogs",
    category="Operations",
)
