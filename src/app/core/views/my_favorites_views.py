# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.my_favorites_models import MyFavorites


class MyFavoritesModelView(ModelView):
    route_base = "/admin/my-favorites"
    datamodel = SQLAInterface(MyFavorites)
    list_columns = ["id", "service", "created_by"]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    MyFavoritesModelView,
    "MyFavorites",
    icon="fa-solid fa-cogs",
    category="Operations",
)
