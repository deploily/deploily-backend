# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_api.models.api_services_model import ApiService
from config import DB_LANGUAGES


class ApiServiceView(ModelView):
    datamodel = SQLAInterface(ApiService)

    list_columns = ["id", "name", "service_slug", "unit_price", "is_published"]
    add_columns = [
        # "category",
        "tags",
        "medias",
        "service_plans",
        "apisix_group_id",
        "myfavorites",
        "name",
        "description",
        *[f"description_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "short_description",
        *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "specifications",
        *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "api_playground_url",
        "service_slug",
        "service_unity",
        "price_category",
        "ratings",
        "is_eligible",
        "is_published",
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
        *[f"description_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "short_description",
        *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "specifications",
        *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "documentation_url",
        "unit_price",
        "image_service",
        "service_slug",
        "service_unity",
        "price_category",
        "curl_command",
        "api_playground_url",
        "service_url",
        "ratings",
        "is_eligible",
        "is_published",
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
        *[f"description_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "short_description",
        *[f"short_description_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "specifications",
        *[f"specifications_{lang}" for lang in DB_LANGUAGES if lang != "en"],
        "documentation_url",
        "unit_price",
        "service_url",
        "image_service",
        "curl_command",
        "api_playground_url",
        "service_slug",
        "service_unity",
        "price_category",
        "ratings",
        "is_eligible",
        "is_published",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    ApiServiceView,
    "Api Services",
    icon="fa-gift",
    category="Master",
)
