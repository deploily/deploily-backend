# -*- coding: utf-8 -*-

from flask import current_app, render_template
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text, event
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import object_session, relationship

from app import db
from app.core.celery_tasks.send_mail_task import send_mail
from app.core.models import Subscription
from app.core.models.mail_models import Mail


class SubscriptionAppService(Subscription):
    __tablename__ = "subscription_app_service"
    id = Column(Integer, ForeignKey("subscription.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "subscription_app_service",
    }
    type = Column(String(50), default="subscription_app_service", nullable=False)

    application_status = Column(
        Enum("processing", "deployed", "error", name="application_status"),
        default="processing",
    )
    required_restart = Column(Boolean, default=False)
    access_url = Column(String(100))
    deployment_error = Column("error", Text())

    version_id = Column(Integer, ForeignKey("version.id"))
    version = relationship("Version", back_populates="app_subscriptions")
    console_url = Column(String(50))
    demo_url = Column(String(255), nullable=True)
    ressource_service_plan_id = Column(Integer, ForeignKey("service_plan.id"))

    ressource_service_plan = relationship("ServicePlan")


_pending_deployed_apps = {}


@event.listens_for(SubscriptionAppService, "after_update")
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
