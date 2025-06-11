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
        "ssh_access",
        "monitoring",
        "ratings",
        "recommended_apps",
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
        "ssh_access",
        "monitoring",
        "ratings",
        "recommended_apps",
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
        "ssh_access",
        "monitoring",
        "ratings",
        "average_rating",
        "recommended_apps",
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
