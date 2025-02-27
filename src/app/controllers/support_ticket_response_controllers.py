# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app.models.support_ticket_response_models import SupportTicketResponse
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_support_ticket_display_columns = [
    "id",
    "message",
    "support_ticket",
    "support_ticket_id",
    "created_on",
    "created_by",
]


class SupportTicketResponseModelApi(ModelRestApi):
    resource_name = "SupportTicketResponse"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(SupportTicketResponse)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = _support_ticket_display_columns
    list_columns = _support_ticket_display_columns
    edit_columns = _support_ticket_display_columns
    _exclude_columns = [
        "changed_by",
        "changed_on",
    ]


appbuilder.add_api(SupportTicketResponseModelApi)
