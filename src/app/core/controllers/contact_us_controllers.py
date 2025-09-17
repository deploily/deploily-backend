# -*- coding: utf-8 -*-

import logging

from flask import current_app, render_template, request
from flask_appbuilder.api import BaseApi, ModelRestApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.celery_tasks.send_mail_task import send_mail
from app.core.models.contact_us_models import ContactUs
from app.core.models.mail_models import Mail

_logger = logging.getLogger(__name__)
_contact_us_display_columns = ["name", "email", "message", "phone", "ressource_id", "created_on"]


class ContactUSModelApi(ModelRestApi):
    resource_name = "contact-us"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ContactUs)
    add_columns = ["name", "email", "message", "phone", "ressource_id"]
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


class PublicContactUSModelApi(BaseApi):

    resource_name = "contact-us-public"

    @expose("/", methods=["POST"])
    def add_contact_us(self):
        """
        Public Contact Us endpoint
        ---
        post:
          summary: Submit a contact us request
          description: Public endpoint to create a contact us record.
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    ressource_id:
                      type: integer
                      description: ressource_id
                    phone:
                      type: string
                      description: phone
                    email:
                      type: string
                      description: email
                    message:
                      type: string
                      description: message
                    name:
                      type: string
                      description: name
          responses:
            200:
              description: Contact created successfully
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
            400:
              description: Bad request
            500:
              description: Internal server error
        """
        try:
            data = request.json

            # create ContactUs object
            item = ContactUs(
                email=data.get("email"),
                message=data.get("message"),
                name=data.get("name"),
                phone=data.get("phone"),
                ressource_id=data.get("ressource_id"),
            )
            db.session.add(item)
            db.session.commit()

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

            # ✅ Return saved object as JSON
            return self.response(
                200,
                result={
                    "id": item.id,
                    "email": item.email,
                    "message": item.message,
                    "name": item.name,
                    "phone": item.phone,
                    "ressource_id": item.ressource_id,
                },
            )
        except Exception as e:
            _logger.error(f"Error in add_contact_us: {e}", exc_info=True)
            db.session.rollback()
            return self.response_500(message="Internal Server Error")


# Register API
appbuilder.add_api(PublicContactUSModelApi)
