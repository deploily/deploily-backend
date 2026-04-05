# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_deployment.models.deployment_services_model import DeploymentService


class DeploymentServiceView(ModelView):
    datamodel = SQLAInterface(DeploymentService)

    list_columns = [
        "id",
        "name",
        "service_slug",
        "unit_price",
        "is_published",
        "sequence",
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
        "is_published",
        "is_eligible",
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
        "is_published",
        "is_eligible",
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
        "is_published",
        "is_eligible",
    ]

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    DeploymentServiceView,
    "Deployment services",
    icon="fa-gift",
    category="Master",
)
