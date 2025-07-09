# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_apps.models.apps_services_model import AppService


class AppServiceView(ModelView):
    datamodel = SQLAInterface(AppService)

    list_columns = ["tags", "name", "unit_price", "average_rating", "is_published"]
    add_columns = [
        # "category",
        "medias",
        "tags",
        "service_plans",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "service_slug",
        "minimal_cpu",
        "minimal_ram",
        "minimal_disk",
        "ratings",
        "recommended_apps",
        "is_eligible",
        "app_versions",
        "is_published",
    ]
    edit_columns = [
        # "category",
        "medias",
        "tags",
        "service_plans",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "service_slug",
        "minimal_cpu",
        "minimal_ram",
        "minimal_disk",
        "ratings",
        "recommended_apps",
        "is_eligible",
        "app_versions",
        "is_published",
    ]
    show_columns = [
        # "category",
        "medias",
        "tags",
        "service_plans",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "service_slug",
        "minimal_cpu",
        "minimal_ram",
        "minimal_disk",
        "ratings",
        "average_rating",
        "recommended_apps",
        "app_versions",
        "is_eligible",
        "is_published",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    AppServiceView,
    "Application Services",
    icon="fa-cogs",
    category="Master",
)
