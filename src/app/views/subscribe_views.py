# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.subscription_models import Subscription


class SubscriptionModelView(ModelView):
    route_base = "/admin/Subscription"
    datamodel = SQLAInterface(Subscription)
    list_columns = ["id", "start_date", "status", "total_amount", "price", "duration_month"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    SubscriptionModelView,
    "Subscription",
    icon="fa-solid fa-sliders",
    category="Service",
)
