# -*- coding: utf-8 -*-

import logging

from flask import current_app, render_template
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.celery_tasks.send_mail_task import send_mail
from app.core.models.contact_us_models import ContactUs
from app.core.models.mail_models import Mail

_logger = logging.getLogger(__name__)
_contact_us_display_columns = ["id", "name", "email", "message", "created_on"]


class ContactUSModelApi(ModelRestApi):
    resource_name = "contact-us"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ContactUs)
    add_columns = ["id", "name", "email", "message"]
    list_columns = _contact_us_display_columns
    edit_columns = _contact_us_display_columns
    _exclude_columns = ["changed_by", "changed_on", "created_by.id"]

    def post_add(self, item: ContactUs):
        """
        Called after a contact us is successfully created.
        """

        try:

            contact_us_template = render_template("emails/contact_us.html", item=item)

            email = Mail(
                title=f"New Contact US Created by {item.name}",
                body=contact_us_template,
                email_to=current_app.config["NOTIFICATION_EMAIL"],
                email_from=current_app.config["NOTIFICATION_EMAIL"],
                mail_state="outGoing",
            )

            db.session.add(email)
            db.session.commit()
            send_mail.delay(email.id)
            _logger.info(f"[EMAIL] Queued email for contact us {item.id}")

        except Exception as e:

            _logger.error(f"[EMAIL] Failed to create email for contact us {item.id}: {e}")


appbuilder.add_api(ContactUSModelApi)
