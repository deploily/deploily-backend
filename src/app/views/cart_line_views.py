# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app import db
from app.models.cart_line_models import CartLine


class CartLineModelView(ModelView):
    route_base = "/admin/cartLine"
    datamodel = SQLAInterface(CartLine)
    list_columns = ["id", "start_date", "amount",
                    "duration_month", "service", "cart"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    CartLineModelView,
    "Cart Line",
    icon="fa-solid fa-sliders",
    category="Cart",
)
