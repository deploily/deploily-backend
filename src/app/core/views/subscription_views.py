# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.subscription_models import Subscription


class SubscriptionModelView(ModelView):
    route_base = "/admin/Subscription"
    datamodel = SQLAInterface(Subscription)
    list_columns = [
        "id",
        "created_by",
        "service_plan",
        "total_amount",
        "status",
        "is_expired",
        "start_date",
        "duration_month",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    SubscriptionModelView,
    "Subscription",
    icon="fa-solid fa-sliders",
    category="Operations",
)
