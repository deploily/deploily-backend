import logging

from flask_appbuilder.api import BaseApi, ModelRestApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.service_apps.models.recommendation_app_services import RecommendationAppService

_logger = logging.getLogger(__name__)

recommendation_display_columns = ["id", "app_services"]


class AppRecommendationModelApi(ModelRestApi):
    resource_name = "app-recommendation"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(RecommendationAppService)
    add_columns = recommendation_display_columns
    list_columns = recommendation_display_columns
    edit_columns = recommendation_display_columns
    exclude_route_methods = ("put", "post", "delete", "info")


appbuilder.add_api(AppRecommendationModelApi)


class PublicAppRecommendationModelApi(BaseApi):  # public version
    resource_name = "app-recommendation-public"

    @expose("/<int:id>", methods=["GET"])
    def get_recommendatin_app_services_by_id(self, id):
        """
        ---
        get:
          summary: Get a specific APP service recommendation by ID
          description: Returns one RecommendationAppService with its associated AppServices
          parameters:
          - in: path
            name: id
            required: true
            schema:
                type: integer
            description: ID of the RecommendationAppService


          responses:
            200:
              description: RecommendationAppService found
              content:
                application/json:
                  schema:
                    type: object

                    properties:
                        id:
                          type: integer
                        app_services:
                          type: array
                          items:
                            type: object
                            properties:
                              id:
                                type: integer
                              image_service:
                                type: string
                              unit_price:
                                type: number
                              documentation_url:
                                type: string
                              tags:
                                type: array
                                items:
                                  type: string
                              service_plans:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    id:
                                      type: integer
                                    name:
                                      type: string
                                    price:
                                      type: number
                                    description:
                                      type: string
                              name:
                                type: string
                              specifications:
                                type: string
                              ssh_access:
                                type: string
                              monitoring:
                                type: string
                              average_rating:
                                type: number
                              name:
                              type: string

            500:
              description: Internal server error
            404:
              description: RecommendationAppService not found
        """
        recommendation = db.session.query(RecommendationAppService).get(id)

        if not recommendation:
            return self.response(404, message="RecommendationAppService not found")

        result = {
            "id": recommendation.id,
            "app_services": [
                {
                    "id": app_service.id,
                    "unit_price": app_service.unit_price,
                    "documentation_url": app_service.documentation_url,
                    "tags": [tag.name for tag in app_service.tags],
                    "service_plans": [
                        {
                            "id": plan.id,
                            "price": plan.price,
                            "is_custom": plan.is_custom,
                            "options": [
                                {
                                    "id": option.id,
                                    "name": option.name,
                                    "value": option.value,
                                }
                                for option in plan.options
                            ],
                        }
                        for plan in app_service.service_plans
                    ],
                    "name": app_service.name,
                    "short_description": app_service.short_description,
                    "description": app_service.description,
                    "image_service": app_service.image_service,
                    "specifications": app_service.specifications,
                    "ssh_access": app_service.ssh_access,
                    "monitoring": app_service.monitoring,
                    "average_rating": app_service.average_rating,
                    "medias": [
                        {
                            "id": media.id,
                            "name": media.title,
                            "image": media.image,
                        }
                        for media in app_service.medias
                    ],
                }
                for app_service in recommendation.app_services
            ],
        }

        return self.response(200, result=result)


appbuilder.add_api(PublicAppRecommendationModelApi)
