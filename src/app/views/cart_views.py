# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.cart_models import Cart


class CartModelView(ModelView):
    route_base = "/admin/cart"
    datamodel = SQLAInterface(Cart)
    list_columns = ["id", "status", "total_amount", "cart_lines"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    CartModelView,
    "Cart",
    icon="fa-solid fa-sliders",
    category="Cart",
)
