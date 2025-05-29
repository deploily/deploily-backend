# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.services_ressources_category_model import (
    ServiceRessouceCategory,
)

_logger = logging.getLogger(__name__)

_service_category_value_display_columns = [
    "id",
    "name",
    "description",
    "short_description",
    "ressouce_services",
]


class ServiceRessouceCategoryModelApi(ModelRestApi):
    resource_name = "ressource-category"
    datamodel = SQLAInterface(ServiceRessouceCategory)
    add_columns = _service_category_value_display_columns
    list_columns = _service_category_value_display_columns
    show_columns = _service_category_value_display_columns
    edit_columns = _service_category_value_display_columns
    exclude_route_methods = ["get", "put", "post", "get_list"]

    @expose("/all", methods=["GET"])
    def get_all_categories(self):
        """
        ---
        get:
        summary: Get all service categories with full ressource_services including provider
        description: Returns a list of all service resource categories with ressource_services and their providers.
        responses:
            200:
            description: A list of service categories
            content:
                application/json:
                schema:
                    type: array
                    items:
                    type: object
                    properties:
                        id:
                        type: integer
                        name:
                        type: string
                        short_description:
                        type: string
                        description:
                        type: string
                        ressource_services:
                        type: array
                        items:
                            type: object
                            additionalProperties: true
            500:
            description: Internal server error
        """
        session = self.appbuilder.get_session
        categories = session.query(ServiceRessouceCategory).all()

        def serialize_sqlalchemy_obj(obj):
            result = {}
            for key in obj.__mapper__.c.keys():
                result[key] = getattr(obj, key)
            if hasattr(obj, "provider") and obj.provider is not None:
                result["provider"] = serialize_sqlalchemy_obj(obj.provider)
            return result

        result = []
        for cat in categories:
            result.append(
                {
                    "id": cat.id,
                    "name": cat.name,
                    "short_description": cat.short_description,
                    "description": cat.description,
                    "ressource_services": [
                        serialize_sqlalchemy_obj(s) for s in cat.ressouce_services
                    ],
                    "medias": [serialize_sqlalchemy_obj(m) for m in cat.medias],
                }
            )

        return self.response(200, result=result)


appbuilder.add_api(ServiceRessouceCategoryModelApi)
