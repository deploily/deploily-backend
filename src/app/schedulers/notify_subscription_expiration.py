import logging
import os
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from flask import current_app as app
from flask import render_template

from app import app, db, scheduler
from app.core.models.subscription_models import Subscription
from app.services.mail_service import send_and_log_email

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@scheduler.task("cron", id="notify_expiring_subscriptions", max_instances=1, minute="*/1")
def notify_expiring_subscriptions():
    print(">>> [CRON] notify_expiring_subscriptions() running")

    def was_already_sent_today(sub_id, days):
        path = f"/tmp/sub_notify_{sub_id}_{days}_{today}.lock"
        return os.path.exists(path)

    def mark_sent(sub_id, days):
        path = f"/tmp/sub_notify_{sub_id}_{days}_{today}.lock"
        with open(path, "w") as f:
            f.write("sent")

    try:

        with app.app_context():
            notice_days = [3, 5, 6, 7, 15, 30]

            subs = (
                db.session.query(Subscription)
                .filter(Subscription.status == "active", Subscription.start_date != None)
                .all()
            )

            for sub in subs:
                try:
                    today = datetime.now().date()
                    end_date = (sub.start_date + relativedelta(months=sub.duration_month)).date()

                    days_difference = (end_date - today).days
                    if days_difference in notice_days:
                        user = sub.created_by

                        if was_already_sent_today(sub.id, days_difference):
                            print(
                                f"[SKIP] Email already sent today for subscription {sub.id} at day {days_difference}"
                            )
                            continue

                        expiration_date = sub.start_date + timedelta(days=30 * sub.duration_month)

                        print(
                            f"[NOTIFY] Subscription ID {sub.id} for user {user.username} expires in {days_difference} days."
                        )

                        subject = f"Your subscription will expire in {days_difference} days"
                        body = render_template(
                            "emails/subscription_expiring.html",
                            user=user,
                            subscription=sub,
                            days=days_difference,
                            expiration_date=expiration_date.strftime("%Y-%m-%d"),
                        )
                        send_and_log_email(user.email, subject, body)

                        mark_sent(sub.id, days_difference)
                except Exception as e:
                    logger.error(f"Error processing subscription {sub.id}: {e}")
                    continue

    except Exception as e:
        logger.error(f"Error in notify_expiring_subscriptions: {e}")
        raise
