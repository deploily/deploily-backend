# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.support_ticket_models import SupportTicket


class SupportTicketModelView(ModelView):
    route_base = "/admin/supportticket"
    datamodel = SQLAInterface(SupportTicket)
    list_columns = ["id", "title", "description", "status", "image", "subscription_id"]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    SupportTicketModelView,
    "SupportTicket",
    icon="fa-solid fa-cogs",
    category="Support Ticket",
)
