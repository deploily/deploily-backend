# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_apps.models.apps_services_model import AppService


class AppServiceView(ModelView):
    datamodel = SQLAInterface(AppService)

    list_columns = ["tags", "name", "unit_price", "average_rating"]
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
        "is_illigible",
        "app_versions",
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
        "is_illigible",
        "app_versions",
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
        "app_versions" "is_illigible",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    AppServiceView,
    "App Services",
    icon="fa-cogs",
    category="Master",
)
