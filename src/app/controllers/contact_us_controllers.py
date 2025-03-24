# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.contact_us_models import ContactUs, FeedbackContact, SupportContact

_logger = logging.getLogger(__name__)
_contact_us_display_columns = ["id", "name", "email", "message", "created_on"]


class ContactUSModelApi(ModelRestApi):
    resource_name = "contact-us"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ContactUs)

    # Ajouter les champs spécifiques aux sous-classes
    add_columns = ["name", "email", "message", "type"]
    list_columns = _contact_us_display_columns + ["type"]
    edit_columns = _contact_us_display_columns

    _exclude_columns = ["changed_by", "changed_on", "created_by.id"]

    def pre_add(self, item):
        """Forcer le bon type avant d'insérer un élément"""
        if item.type == "support_contact":
            item.__class__ = SupportContact
        elif item.type == "feedback_contact":
            item.__class__ = FeedbackContact
        else:
            item.__class__ = ContactUs

    def pre_update(self, item):
        """S'assurer que l'objet mis à jour garde son bon type"""
        existing = self.datamodel.get(item.id)
        if existing:
            item.__class__ = existing.__class__


appbuilder.add_api(ContactUSModelApi)
