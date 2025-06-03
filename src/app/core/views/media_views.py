# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.media_models import Media


class MediaModelView(ModelView):
    route_base = "/admin/media"
    datamodel = SQLAInterface(Media)
    list_columns = [
        "id",
        "title",
    ]


db.create_all()
appbuilder.add_view(
    MediaModelView,
    "Media",
    icon="fa-solid fa-cogs",
    category="Master",
)
