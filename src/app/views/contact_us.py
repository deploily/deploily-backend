# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.contact_us_models import ContactUs, FeedbackContact, SupportContact


# 📌 Vue pour tous les types de contacts
class ContactUsModelView(ModelView):
    route_base = "/admin/contact-us"
    datamodel = SQLAInterface(ContactUs)
    list_columns = ["id", "name", "email", "message", "type"]  # Ajout du champ type
    base_order = ("id", "desc")


# 📌 Vue spécifique pour les contacts de type Support
class SupportContactModelView(ModelView):
    route_base = "/admin/support-contact"
    datamodel = SQLAInterface(SupportContact)
    list_columns = ["id", "name", "email", "message", "issue_type"]  # Ajout de issue_type
    base_order = ("id", "desc")


# 📌 Vue spécifique pour les contacts de type Feedback
class FeedbackContactModelView(ModelView):
    route_base = "/admin/feedback-contact"
    datamodel = SQLAInterface(FeedbackContact)
    list_columns = ["id", "name", "email", "message", "rating"]  # Ajout de rating
    base_order = ("id", "desc")


# 🚀 Ajouter les vues à Flask AppBuilder
db.create_all()
appbuilder.add_view(
    ContactUsModelView, "Tous les Contacts", icon="fa-solid fa-envelope", category="Contact US"
)
appbuilder.add_view(
    SupportContactModelView, "Contacts Support", icon="fa-solid fa-headset", category="Contact US"
)
appbuilder.add_view(
    FeedbackContactModelView, "Contacts Feedback", icon="fa-solid fa-comment", category="Contact US"
)
