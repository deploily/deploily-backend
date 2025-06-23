# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_api.models.api_service_subscription_model import ApiServiceSubscription


class ApiServiceSubscriptionView(ModelView):
    datamodel = SQLAInterface(ApiServiceSubscription)

    list_columns = [
        "id",
        "created_by",
        "price",
        "total_amount",
        "status",
        "is_expired",
        "start_date",
        "duration_month",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    ApiServiceSubscriptionView,
    "Api Service Subscriptions",
    icon="fa-cogs",
    category="Apis",
)
