# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.support_ticket_response_models import SupportTicketResponse


class SupportTicketResponseModelView(ModelView):
    route_base = "/admin/supportticket-response"
    datamodel = SQLAInterface(SupportTicketResponse)
    list_columns = ["id", "message", "support_ticket"]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    SupportTicketResponseModelView,
    "SupportTicketMessage",
    icon="fa-solid fa-cogs",
    category="Support Ticket",
)
