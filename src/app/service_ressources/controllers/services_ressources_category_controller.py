# -*- coding: utf-8 -*-

import logging

from flask import request
from flask_appbuilder.api import ModelRestApi, expose
from flask_appbuilder.models.sqla.filters import FilterEqual
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import or_

from app import appbuilder, db
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
    "list_providers",
    "logo",
    "min_category_price",
]


class ServiceRessouceCategoryModelApi(ModelRestApi):
    resource_name = "ressource-category"
    datamodel = SQLAInterface(ServiceRessouceCategory)
    add_columns = _service_category_value_display_columns
    list_columns = _service_category_value_display_columns
    show_columns = _service_category_value_display_columns
    edit_columns = _service_category_value_display_columns
    exclude_route_methods = ["get", "put", "post", "get_list"]
    search_columns = ["name", "description"]

    base_filters = [["is_published", FilterEqual, True]]

    @expose("/all", methods=["GET"])
    def get_all_categories(self):
        """
        ---
        get:
          summary: Get all service categories with full ressource_services including provider
          description: Returns a list of all service resource categories with ressource_services and their providers.
          parameters:
            - in: query
              name: search_value
              schema:
                type: string
              required: false
              description: Filter categories by name or description (partial match)
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
                        medias:
                          type: array
                          items:
                            type: object
                            additionalProperties: true
            500:
              description: Internal server error
        """
        search_value = request.args.get("search_value")
        query = db.session.query(ServiceRessouceCategory)

        if search_value:
            query = query.filter(
                or_(
                    ServiceRessouceCategory.name.ilike(f"%{search_value}%"),
                    ServiceRessouceCategory.description.ilike(f"%{search_value}%"),
                )
            )

        # categories = query.all()
        categories = query.filter(ServiceRessouceCategory.is_published.is_(True)).all()

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
                    "logo": cat.logo,
                    "min_category_price": cat.min_category_price,
                    "description": cat.description,
                    "providers_list": cat.list_providers,
                    # "ressource_services": [
                    #     serialize_sqlalchemy_obj(s) for s in cat.ressouce_services
                    # ],
                    "medias": [serialize_sqlalchemy_obj(m) for m in cat.medias],
                }
            )
        return self.response(200, result=result)


appbuilder.add_api(ServiceRessouceCategoryModelApi)
