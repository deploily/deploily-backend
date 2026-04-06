from datetime import datetime

from flask import render_template

from app import app, db, scheduler
from app.core.models.managed_ressource_models import ManagedRessource
from app.services.mail_service import send_and_log_email

sent_ressource_notifications = set()
last_reset_date_ressource = None
notice_days = [3, 5, 6, 7, 15, 30]


@scheduler.task("cron", id="notify_managed_ressource_expiration", max_instances=1, hour=7, minute=0)
def notify_managed_ressource_expiration():
    global sent_ressource_notifications, last_reset_date_ressource

    today = datetime.now().date()

    # Reset daily sent cache
    if last_reset_date_ressource != today:
        sent_ressource_notifications.clear()
        last_reset_date_ressource = today

    try:
        with app.app_context():
            resources = db.session.query(ManagedRessource).all()
            for res in resources:
                try:

                    if not res.end_date:
                        continue  # skip resources without an end date

                    days_remaining = (res.end_date - today).days

                    if days_remaining not in notice_days:
                        continue

                    key = (res.id, days_remaining, today)
                    if key in sent_ressource_notifications:
                        print(f"[SKIP] Already notified for resource {res.host_name} ({res.ip})")
                        continue

                    user = res.access_user
                    if not user:
                        print(f"[WARN] Resource {res.host_name} has no access_user assigned")
                        continue

                    print(
                        f"[NOTIFY] Resource {res.host_name} ({res.ip}) expires in {days_remaining} days for user {user.username}"
                    )

                    subject = f"Managed Resource Subscription Expiring in {days_remaining} Days"
                    body = render_template(
                        "emails/managed_ressource_expiring.html",
                        user=user,
                        resource=res,
                        days=days_remaining,
                        expiration_date=res.end_date.strftime("%Y-%m-%d"),
                    )

                    send_and_log_email(user.email, subject, body)
                    sent_ressource_notifications.add(key)

                except Exception as e:
                    print(f"Error processing resource {res.id}: {e}")
                    continue

    except Exception as e:
        print(f"Error in notify_managed_ressource_expiration: {e}")
        raise
