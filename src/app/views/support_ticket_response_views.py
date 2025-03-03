# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.support_ticket_response_models import SupportTicketResponse


class SupportTicketResponseModelView(ModelView):
    route_base = "/admin/supportticket-response"
    datamodel = SQLAInterface(SupportTicketResponse)
    list_columns = ["id", "message", "support_ticket"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    SupportTicketResponseModelView,
    "SupportTicketResponse",
    icon="fa-solid fa-cogs",
    category="Support Ticket",
)
