# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_deployment.models.deployment_services_model import DeploymentService


class DeploymentServiceView(ModelView):
    datamodel = SQLAInterface(DeploymentService)

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
        "service_unity",
        "price_category",
        "deployment_field",
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
        "service_unity",
        "price_category",
        "deployment_field",
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
        "service_unity",
        "price_category",
        "deployment_field",
        "ratings",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    DeploymentServiceView,
    "Cicd",
    icon="fa-cogs",
    category="Master",
)
