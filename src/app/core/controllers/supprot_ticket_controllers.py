import logging

from flask import current_app, render_template
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import current_user

from app import appbuilder, db
from app.core.models.mail_models import Mail
from app.core.models.support_ticket_models import SupportTicket
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_support_ticket_display_columns = [
    "id",
    "title",
    "status",
    "description",
    "image",
    "subscription_id",
    "subscription",
    "created_on",
    "support_ticket_responses",
]


class SupportTicketModelApi(ModelRestApi):
    resource_name = "support-ticket"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(SupportTicket)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    add_columns = [
        "id",
        "title",
        "status",
        "description",
        "image",
        "subscription_id",
        "subscription",
        "support_ticket_responses",
    ]
    list_columns = _support_ticket_display_columns
    edit_columns = _support_ticket_display_columns
    _exclude_columns = [
        "changed_on",
        "created_by",
        "changed_by",
    ]

    def post_add(self, item: SupportTicket):
        """
        Called after a support ticket is successfully created.
        """
        try:
            user = current_user
            support_tickert_template = render_template(
                "emails/support_ticket.html", item=item, user=user
            )

            email = Mail(
                title=f"New Support Ticket Created By {user.first_name} {user.last_name}",
                body=support_tickert_template,
                email_to=current_app.config["NOTIFICATION_EMAIL"],
                email_from=current_app.config["NOTIFICATION_EMAIL"],
                mail_state="outGoing",
            )
            db.session.add(email)
            db.session.commit()
            _logger.info(f"[EMAIL] Queued email for support ticket {item.id}")
        except Exception as e:
            _logger.error(f"[EMAIL] Failed to create email for support ticket {item.id}: {e}")


appbuilder.add_api(SupportTicketModelApi)
