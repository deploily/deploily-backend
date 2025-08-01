# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_ressources.models.services_ressources_model import RessourceService


class RessourceServiceView(ModelView):
    datamodel = SQLAInterface(RessourceService)

    list_columns = [
        "name",
        "provider",
        "unit_price",
        "discount",
        "tags",
        "is_published",
    ]
    add_columns = [
        # "category",
        "tags",
        "service_plans",
        "provider",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "discount",
        "service_slug",
        "service_unity",
        "price_category",
        "ressource_field",
        "is_published",
    ]
    edit_columns = [
        # "category",
        "tags",
        "service_plans",
        "provider",
        "myfavorites",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "discount",
        "service_slug",
        "service_unity",
        "price_category",
        "ressource_field",
        "is_published",
    ]
    show_columns = [
        # "category",
        "tags",
        "service_plans",
        "myfavorites",
        "provider",
        "name",
        "description",
        "short_description",
        "specifications",
        "documentation_url",
        "unit_price",
        "image_service",
        "discount",
        "service_slug",
        "service_unity",
        "price_category",
        "ressource_field",
        "is_published",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    RessourceServiceView,
    "Ressources",
    icon="fa-cogs",
    category="Master",
)
