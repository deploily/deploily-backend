# -*- coding: utf-8 -*-

from flask import request
from flask_appbuilder.api import expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import or_

from app import appbuilder, db
from app.core.controllers.service_controllers import ServiceModelApi
from app.service_api.models.api_services_model import ApiService

api_columns = [
    "curl_command",
    "service_url",
    "api_playground_url",
    "average_rating",
    "is_subscribed",
    "min_api_price",
]


class ApiServiceModelApi(ServiceModelApi):
    resource_name = "api-service"
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
          summary: Get all API services
          description: Returns a list of ApiService with name, short_description, description, service_plans and medias
          parameters:
            - in: query
              name: search_value
              schema:
                type: string
              required: false
              description: Filter categories by name or description (partial match)
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
        search_value = request.args.get("search_value")
        query = db.session.query(ApiService)
        if search_value:
            query = query.filter(
                or_(
                    ApiService.name.ilike(f"%{search_value}%"),
                    ApiService.description.ilike(f"%{search_value}%"),
                )
            )

        # services = query.all()
        services = query.filter(ApiService.is_published.is_(True)).all()

        def serialize_service(service):
            return {
                "name": service.name,
                "short_description": service.short_description,
                "description": service.description,
                "image_service": service.image_service,
                "documentation_url": service.documentation_url,
                "min_api_price": service.min_api_price,
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
