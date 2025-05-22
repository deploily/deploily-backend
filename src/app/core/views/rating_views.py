# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.rating_models import Rating


class RatingModelView(ModelView):
    route_base = "/admin/rating"
    datamodel = SQLAInterface(Rating)
    list_columns = ["id", "comment"]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    RatingModelView,
    "Rating",
    icon="fa-solid fa-cogs",
    category="Contact US ",
)
