# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_api.models.api_services_model import ApiService


class ApiServiceView(ModelView):
    datamodel = SQLAInterface(ApiService)

    list_columns = ["tags", "name", "unit_price"]
    add_columns = [
        # "category",
        "tags",
        "medias",
        "service_plans",
        "apisix_group_id",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "api_playground_url",
        "service_slug",
        "ratings",
    ]
    edit_columns = [
        # "category",
        "medias",
        "tags",
        "service_plans",
        "apisix_group_id",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "service_slug",
        "curl_command",
        "api_playground_url",
        "service_url",
        "ratings",
    ]
    show_columns = [
        # "category",
        "medias",
        "tags",
        "service_plans",
        "apisix_group_id",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "api_playground_url",
        "service_slug",
        "ratings",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    ApiServiceView,
    "Api Services",
    icon="fa-cogs",
    category="Master",
)
