# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.contact_us_models import ContactUs


class ContactUsModelView(ModelView):
    route_base = "/admin/contact-us"
    datamodel = SQLAInterface(ContactUs)
    list_columns = ["id", "name", "email", "message"]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    ContactUsModelView,
    "Contact Us ",
    icon="fa-solid fa-cogs",
    category="Contact US ",
)
