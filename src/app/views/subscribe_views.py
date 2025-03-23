# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.subscribe_models import Subscribe


class SubscribeModelView(ModelView):
    route_base = "/admin/subscribe"
    datamodel = SQLAInterface(Subscribe)
    list_columns = ["id", "start_date", "status", "total_amount", "price", "duration_month"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    SubscribeModelView,
    "Subscribe",
    icon="fa-solid fa-sliders",
    category="Service",
)
