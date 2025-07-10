# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.core.models.service_models import Service


class ServiceModelView(ModelView):
    route_base = "/admin/Service"
    datamodel = SQLAInterface(Service)
    list_columns = [
        "id",
        "name",
        "documentation_url",
        "unit_price",
        "is_in_favorite",
        "is_eligible",
        "is_published",
    ]

    base_permissions = ["can_list", "can_show"]  # only allow viewing

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


db.create_all()
appbuilder.add_view(
    ServiceModelView,
    "Service",
    icon="fa-solid fa-cogs",
    category="Master",
)
