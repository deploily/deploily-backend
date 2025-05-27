# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.comment_models import Comment


class CommentModelView(ModelView):
    route_base = "/admin/comment"
    datamodel = SQLAInterface(Comment)
    list_columns = ["id", "comment"]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    CommentModelView,
    "Comment",
    icon="fa-solid fa-cogs",
    category="Contact US ",
)
