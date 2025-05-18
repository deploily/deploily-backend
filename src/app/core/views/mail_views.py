# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.mail_models import Mail


class MailModelView(ModelView):
    route_base = "/admin/mail"
    datamodel = SQLAInterface(Mail)
    list_columns = ["id", "title", "body", "mail_state", "email_from", "email_to"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    MailModelView,
    "Mail ",
    icon="fa-solid fa-cogs",
    category="Contact US ",
)
