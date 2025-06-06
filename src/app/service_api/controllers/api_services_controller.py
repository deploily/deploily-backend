# -*- coding: utf-8 -*-

from flask_appbuilder.api import expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.controllers.service_controllers import ServiceModelApi
from app.service_api.models.api_services_model import ApiService

api_columns = ["curl_command", "service_url", "api_playground_url", "average_rating"]


class ApiServiceModelApi(ServiceModelApi):
    resource_name = "api_service"
    datamodel = SQLAInterface(ApiService)

    add_columns = ServiceModelApi.add_columns + api_columns
    list_columns = ServiceModelApi.list_columns + api_columns
    show_columns = ServiceModelApi.show_columns + api_columns
    edit_columns = ServiceModelApi.edit_columns + api_columns

    @expose("/all", methods=["GET"])
    def get_all_api_services(self):
        """
        ---
        get:
          summary: Get all API services (base fields + service_plans + medias)
          description: Returns a list of ApiService with name, short_description, description, service_plans and medias
          responses:
            200:
              description: List of ApiServices
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: string
                        short_description:
                          type: string
                        description:
                          type: string
                        service_plans:
                          type: array
                          items:
                            type: object
                            additionalProperties: true
                        medias:
                          type: array
                          items:
                            type: object
                            additionalProperties: true
            500:
              description: Internal server error
        """
        services = db.session.query(ApiService).all()

        def serialize_service(service):
            return {
                "name": service.name,
                "short_description": service.short_description,
                "description": service.description,
                "image_service": service.image_service,
                "specifications": service.specifications,
                "service_plans": [
                    {
                        "id": plan.id,
                        "name": plan.plan.name,
                        "price": plan.price,
                    }
                    for plan in service.service_plans
                ],
                "medias": [
                    {
                        "id": media.id,
                        "name": media.title,
                        "image": media.image,
                    }
                    for media in service.medias
                ],
            }

        result = [serialize_service(s) for s in services]
        return self.response(200, result=result)

    # @expose("/custom_endpoint", methods=["GET"])
    # def custom_endpoint(self):
    #     return self.response(200, message="Custom API for ApiService")


appbuilder.add_api(ApiServiceModelApi)
