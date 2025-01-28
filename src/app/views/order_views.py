# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app import db
from app.models.order_models import Order


class OrderModelView(ModelView):
    route_base = "/admin/order"
    datamodel = SQLAInterface(Order)
    list_columns = ["id", "status"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    OrderModelView,
    "order",
    icon="fa-solid fa-sliders",
    category="order",
)