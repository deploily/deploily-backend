# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app import db
from app.models.cart_models import Cart


class CartModelView(ModelView):
    route_base = "/admin/cart"
    datamodel = SQLAInterface(Cart)
    list_columns = ["id", "status"]
    base_cart = ("id", "desc")


db.create_all()
appbuilder.add_view(
    CartModelView,
    "cart",
    icon="fa-solid fa-sliders",
    category="cart",
)