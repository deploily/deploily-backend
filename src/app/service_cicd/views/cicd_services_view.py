# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_cicd.models.cicd_services_model import CicdService


class CicdServiceView(ModelView):
    datamodel = SQLAInterface(CicdService)

    list_columns = [
        "tags",
        "name",
        "unit_price",
    ]
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
        "cicd_field",
        "ratings",
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
        "cicd_field",
        "ratings",
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
        "cicd_field",
        "ratings",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    CicdServiceView,
    "Cicd Services",
    icon="fa-cogs",
    category="Master",
)
