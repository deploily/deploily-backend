import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_apps.models.recommendation import RecommendationAppService

_logger = logging.getLogger(__name__)

recommendation_display_columns = ["id", "app_services"]


class RecommendationAppServiceModelApi(ModelRestApi):
    resource_name = "recommendation"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(RecommendationAppService)
    add_columns = recommendation_display_columns
    list_columns = recommendation_display_columns
    edit_columns = recommendation_display_columns
    exclude_route_methods = ("put", "post", "delete", "info")


appbuilder.add_api(RecommendationAppServiceModelApi)
