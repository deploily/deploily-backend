# -*- coding: utf-8 -*-

from operator import or_

from flask import request
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.controllers.service_controllers import ServiceModelApi
from app.service_deployment.models.deployment_services_model import DeploymentService

deployment_columns = ["deployment_field", "average_rating"]


class DeploymentServiceModelApi(ServiceModelApi):
    resource_name = "deployment-service"
    datamodel = SQLAInterface(DeploymentService)

    add_columns = ServiceModelApi.add_columns + deployment_columns
    list_columns = ServiceModelApi.list_columns + deployment_columns
    show_columns = ServiceModelApi.show_columns + deployment_columns
    edit_columns = ServiceModelApi.edit_columns + deployment_columns
    base_order = ("sequence", "asc")

    def get_all_deployment_services(self):
        """
        ---
        get:
          summary: Get all Deployment services (base fields + service_plans + medias)
          description: Returns a list of DeploymentService with name, short_description, description, service_plans and medias
          parameters:
            - in: query
              name: search_value
              schema:
                type: string
              required: false
          responses:
            200:
              description: List of DeploymentServices
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
        # services = db.session.query(AppService).all()

        search_value = request.args.get("search_value")
        query = db.session.query(DeploymentService)
        if search_value:
            query = query.filter(
                or_(
                    DeploymentService.name.ilike(f"%{search_value}%"),
                    DeploymentService.description.ilike(f"%{search_value}%"),
                )
            )

        # services = query.all()
        services = (
            query.filter(DeploymentService.is_published.is_(True))
            # .order_by(DeploymentService.sequence.asc())
            .all()
        )

        def serialize_service(service):
            return {
                "id": service.id,
                "name": service.name,
                "price_category": service.price_category,
                "demo_url": service.demo_url,
                "short_description": service.short_description,
                "description": service.description,
                "image_service": service.image_service,
                "specifications": service.specifications,
                # ! ADD THESE FIELDS
                # "min_app_price": service.min_app_price,
                # "minimal_cpu": service.minimal_cpu,
                # "minimal_ram": service.minimal_ram,
                # "minimal_disk": service.minimal_disk,
                "service_slug": service.service_slug,
                "average_rating": service.average_rating,
                "is_subscribed": service.is_subscribed,
                "documentation_url": service.documentation_url,
                "unit_price": service.unit_price,
                "deployment_field": service.deployment_field,
                # "recommended_apps": [
                #     {
                #         "id": app.id,
                #     }
                #     for app in service.recommended_apps
                # ],
                # "app_versions": [
                #     {"id": app.id, "version": app.name, "description": app.description}
                #     for app in service.app_versions
                # ],
                "service_plans": [
                    {
                        "id": plan.id,
                        "price": plan.price,
                        "unity": plan.unity,
                        "name": plan.plan.name,
                        "subscription_category": plan.subscription_category,
                        "is_custom": plan.is_custom,
                        "options": [
                            {
                                "id": option.id,
                                "option_type": option.option_type,
                                "option_value": option.option_value,
                                "icon": option.icon,
                                "html_content": option.html_content,
                                "sequence": option.sequence,
                            }
                            for option in plan.options
                        ],
                        "preparation_time": plan.preparation_time,
                    }
                    for plan in sorted(service.service_plans, key=lambda p: p.price or 0)
                ],
                "medias": [
                    {
                        "id": media.id,
                        "name": media.title,
                        "image": media.image,
                        "horizontal_image": media.horizontal_image,
                        "vertical_image": media.vertical_image,
                        "square_image": media.square_image,
                    }
                    for media in service.medias
                ],
            }

        result = [serialize_service(s) for s in services]
        return self.response(200, result=result)


appbuilder.add_api(DeploymentServiceModelApi)


class PublicDeploymentServiceApi(BaseApi):  # public version
    resource_name = "deployment-service-public"

    @expose("/<string:slug>", methods=["GET"])
    def get_deployment_service_by_slug(self, slug):
        """
        ---
        get:
          summary: Get an Deployment service by slug (base fields + service_plans + medias)
          description: Returns a specific DeploymentService by service_slug
          parameters:
            - in: path
              name: slug
              required: true
              schema:
                type: string
          responses:
            200:
              description: DeploymentService found
            404:
              description: DeploymentService not found
        """
        service = db.session.query(DeploymentService).filter_by(service_slug=slug).first()
        if not service:
            return self.response(404, message="DeploymentService not found")

        result = self.serialize_service(service)
        return self.response(200, result=result)

    @expose("/<int:id>", methods=["GET"])
    def get_deployment_service_by_id(self, id):  # <- Use the captured `id` parameter
        """
        ---
        get:
          summary: Get an Deployment service by ID (base fields + service_plans + medias)
          description: Returns a specific DeploymentService with name, short_description, description, service_plans and medias
          parameters:
            - in: path
              name: id
              required: true
              schema:
                type: integer
          responses:
            200:
              description: DeploymentService found
              content:
                application/json:
                  schema:
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
            404:
              description: DeploymentService not found
            500:
              description: Internal server error
        """
        service = db.session.query(DeploymentService).get(id)
        if not service:
            return self.response(404, message="DeploymentService not found")

        def serialize_service(service):
            return {
                "name": service.name,
                "price_category": service.price_category,
                "short_description": service.short_description,
                "description": service.description,
                "image_service": service.image_service,
                "specifications": service.specifications,
                "documentation_url": service.documentation_url,
                "unit_price": service.unit_price,
                # "demo_url": service.demo_url,
                # "minimal_cpu": service.minimal_cpu,
                # "minimal_ram": service.minimal_ram,
                # "minimal_disk": service.minimal_disk,
                "service_slug": service.service_slug,
                "is_subscribed": service.is_subscribed,
                # "app_versions": [
                #     {"id": app.id, "version": app.name, "description": app.description}
                #     for app in service.app_versions
                # ],
                "average_rating": service.average_rating,
                # "recommended_apps": [{"id": app.id} for app in service.recommended_apps],
                "service_plans": [
                    {
                        "id": plan.id,
                        "price": plan.price,
                        "name": plan.plan.name,
                        "subscription_category": plan.subscription_category,
                        "is_custom": plan.is_custom,
                        "options": [
                            {
                                "id": option.id,
                                "option_type": option.option_type,
                                "option_value": option.option_value,
                                "icon": option.icon,
                                "html_content": option.html_content,
                                "sequence": option.sequence,
                            }
                            for option in plan.options
                        ],
                        "preparation_time": plan.preparation_time,
                    }
                    for plan in sorted(service.service_plans, key=lambda p: p.price or 0)
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

        result = serialize_service(service)
        return self.response(200, result=result)

    def serialize_service(self, service):
        return {
            "id": service.id,
            "name": service.name,
            "price_category": service.price_category,
            "short_description": service.short_description,
            "description": service.description,
            "image_service": service.image_service,
            "specifications": service.specifications,
            "documentation_url": service.documentation_url,
            # "demo_url": service.demo_url,
            # "minimal_cpu": service.minimal_cpu,
            # "minimal_ram": service.minimal_ram,
            # "minimal_disk": service.minimal_disk,
            "service_slug": service.service_slug,
            "is_subscribed": service.is_subscribed,
            # "app_versions": [
            #     {"id": app.id, "version": app.name, "description": app.description}
            #     for app in service.app_versions
            # ],
            "average_rating": service.average_rating,
            # "recommended_apps": [{"id": app.id} for app in service.recommended_apps],
            "service_plans": [
                {
                    "id": plan.id,
                    "price": plan.price,
                    "name": plan.plan.name,
                    "subscription_category": plan.subscription_category,
                    "is_custom": plan.is_custom,
                    "options": [
                        {
                            "id": option.id,
                            "option_type": option.option_type,
                            "option_value": option.option_value,
                            "icon": option.icon,
                            "html_content": option.html_content,
                            "sequence": option.sequence,
                        }
                        for option in plan.options
                    ],
                    "preparation_time": plan.preparation_time,
                }
                for plan in sorted(service.service_plans, key=lambda p: p.price or 0)
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


# Register the API with Flask AppBuilder
appbuilder.add_api(PublicDeploymentServiceApi)
