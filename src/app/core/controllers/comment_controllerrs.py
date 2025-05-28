import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.models.comment_models import Comment
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

comment_display_columns = ["id", "comment", "service_id", "service"]


class CommentModelApi(ModelRestApi):
    resource_name = "comment"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Comment)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = comment_display_columns
    list_columns = comment_display_columns
    edit_columns = comment_display_columns
    _exclude_columns = [
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(CommentModelApi)
