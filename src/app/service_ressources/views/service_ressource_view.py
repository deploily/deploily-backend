# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_ressources.models.services_ressources_model import RessourceService


class RessourceServiceView(ModelView):
    datamodel = SQLAInterface(RessourceService)

    list_columns = [
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
        "service_slug",
        "ressource_field",
    ]
    add_columns = [
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
        "service_slug",
        "ressource_field",
    ]
    edit_columns = [
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
        "service_slug",
        "ressource_field",
    ]
    show_columns = [
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
        "service_slug",
        "ressource_field",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    RessourceServiceView,
    "Ressources Services",
    icon="fa-cogs",
    category="Service",
)
