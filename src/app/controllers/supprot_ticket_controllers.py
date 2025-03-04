# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.support_ticket_models import SupportTicket
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_support_ticket_display_columns = [
    "id",
    "title",
    "status",
    "description",
    "image",
    "cart_line_id",
    "cart_line",
    "created_on",
    "support_ticket_responses"
]


class SupportTicketModelApi(ModelRestApi):
    resource_name = "support-ticket"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(SupportTicket)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = [
    "id",
    "title",
    "status",
    "description",
    "image",
    "cart_line_id",
    "cart_line",
    "support_ticket_responses"
]
    list_columns = _support_ticket_display_columns 
    edit_columns = _support_ticket_display_columns
    _exclude_columns = [
        "changed_on",
        "created_by",
        "changed_by",
    ]


appbuilder.add_api(SupportTicketModelApi)
