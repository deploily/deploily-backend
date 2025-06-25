# -*- coding: utf-8 -*-

from flask import current_app, render_template
from sqlalchemy import Column, ForeignKey, Integer, String, Text, event
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import object_session

from app import db
from app.core.celery_tasks.send_mail_task import send_mail
from app.core.models.mail_models import Mail
from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)


class TtkEpaySubscriptionAppService(SubscriptionAppService):
    __tablename__ = "ttk_epay_subscription_app_service"
    id = Column(Integer, ForeignKey("subscription_app_service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "ttk_epay",
    }
    ttk_epay_api_secret_key = Column(String, nullable=True)
    ttk_epay_client_site_url = Column(String, nullable=True)
    ttk_epay_client_site_name = Column(String, nullable=True)
    ttk_epay_client_site_logo_url = Column(String, nullable=True)
    ttk_epay_client_site_privacy = Column(String, nullable=True)
    ttk_epay_client_site_terms = Column(String, nullable=True)
    ttk_epay_client_site_phone_number = Column(String, nullable=True)
    ttk_epay_client_site_address = Column(String, nullable=True)
    ttk_epay_client_site_email = Column(String, nullable=True)
    ttk_epay_satim_server_url = Column(String, nullable=True)
    ttk_epay_satim_base_url = Column(String, nullable=True)
    ttk_epay_satim_fail_url = Column(String, nullable=True)
    ttk_epay_satim_confirm_url = Column(String, nullable=True)
    ttk_epay_satim_client_server_url = Column(String, nullable=True)
    ttk_epay_satim_user_name = Column(String, nullable=True)
    ttk_epay_satim_password = Column(String, nullable=True)
    ttk_epay_satim_terminal_id = Column(String, nullable=True)
    ttk_epay_satim_language = Column(String, nullable=True)
    ttk_epay_satim_description = Column(String, nullable=True)
    ttk_epay_satim_currency = Column(String, nullable=True)
    ttk_epay_satim_json_params = Column(Text, nullable=True)
    ttk_epay_mvc_satim_server_url = Column(String, nullable=True)
    ttk_epay_mvc_satim_fail_url = Column(String, nullable=True)
    ttk_epay_mvc_satim_confirm_url = Column(String, nullable=True)


_pending_deployed_apps = {}


@event.listens_for(TtkEpaySubscriptionAppService, "after_update")
def mark_for_email(mapper, connection, target):
    if target.application_status in ["deployed", "error"]:
        session = object_session(target)
        if session:
            session_id = id(session)
            _pending_deployed_apps.setdefault(session_id, []).append(target)


@event.listens_for(db.session.__class__, "after_commit")
def send_deployed_app_emails(session):
    session_id = id(session)
    targets = _pending_deployed_apps.pop(session_id, [])

    if not targets:
        return

    # Use a new session for email creation
    new_session = SASession(bind=db.engine)
    notify_email = current_app.config.get("NOTIFICATION_EMAIL")

    try:
        for target in targets:
            # Skip if user email is missing
            if not getattr(target.created_by, "email", None):
                print(f"[WARN] User {target.created_by.id} has no email.")
                continue

            if target.application_status == "deployed":
                template = "emails/user_application_deployed.html"
                title = "Your application has been deployed"
                message = ""
            else:
                template = "emails/user_application_failed.html"
                title = "Your application has failed"
                message = target.deployment_error

            # Render email body
            user_body = render_template(
                template, user=target.created_by, application=target.name, message=message
            )

            # Create Mail object
            user_email = Mail(
                title=title,
                body=user_body,
                email_to=target.created_by.email,
                email_from=notify_email,
                mail_state="outGoing",
            )

            new_session.add(user_email)
            new_session.flush()  # Assign ID
            email_id = user_email.id

            new_session.commit()  # Commit before sending
            send_mail.delay(email_id)  # Queue for sending

    except Exception as e:
        new_session.rollback()
        print(f"[Email Send Error] {e}")

    finally:
        new_session.close()
