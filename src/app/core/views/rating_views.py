# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.rating_models import Score


class RatingModelView(ModelView):
    route_base = "/admin/rating"
    datamodel = SQLAInterface(Score)
    list_columns = ["id", "rating"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    RatingModelView,
    "Rating",
    icon="fa-solid fa-cogs",
    category="Contact US ",
)
