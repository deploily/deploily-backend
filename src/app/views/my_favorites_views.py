# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.my_favorites_models import MyFavorites


class MyFavoritesModelView(ModelView):
    route_base = "/admin/my-favorites"
    datamodel = SQLAInterface(MyFavorites)
    list_columns = ["id",  "service"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    MyFavoritesModelView,
    "MyFavorites",
    icon="fa-solid fa-cogs",
    category="My Favorites",
)
