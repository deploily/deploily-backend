import os
from datetime import date, timedelta

from flask import current_app as app
from flask import render_template
from sqlalchemy import Integer, cast, func

from app import app, db, scheduler
from app.core.models.subscription_models import Subscription
from app.services.mail_service import send_and_log_email


@scheduler.task("cron", id="notify_expiring_subscriptions", max_instances=1, minute="*/1")
def notify_expiring_subscriptions():
    print(">>> [CRON] notify_expiring_subscriptions() running")
    today = date.today()

    def was_already_sent_today(sub_id, days):
        path = f"/tmp/sub_notify_{sub_id}_{days}_{today}.lock"
        return os.path.exists(path)

    def mark_sent(sub_id, days):
        path = f"/tmp/sub_notify_{sub_id}_{days}_{today}.lock"
        with open(path, "w") as f:
            f.write("sent")

    with app.app_context():
        notice_days = [3, 7, 15, 30]
        subs = (
            db.session.query(Subscription)
            .filter(
                Subscription.status == "active",
                Subscription.start_date != None,
                cast(func.DATE_PART("day", func.now() - Subscription.start_date), Integer).in_(
                    notice_days
                ),
            )
            .all()
        )

        for sub in subs:
            user = sub.created_by
            days = (today - sub.start_date.date()).days

            if was_already_sent_today(sub.id, days):
                print(f"[SKIP] Email already sent today for subscription {sub.id} at day {days}")
                continue

            expiration_date = sub.start_date + timedelta(days=30 * sub.duration_month)

            print(
                f"[NOTIFY] Subscription ID {sub.id} for user {user.username} expires in {days} days."
            )

            subject = f"Your subscription will expire in {days} days"
            body = render_template(
                "emails/subscription_expiring.html",
                user=user,
                subscription=sub,
                days=days,
                expiration_date=expiration_date.strftime("%Y-%m-%d"),
            )
            send_and_log_email(user.email, subject, body)

            mark_sent(sub.id, days)

        # # Notify users with already expired subscriptions
        expired_subs = (
            db.session.query(Subscription)
            .filter(
                Subscription.status == "active",
                Subscription.start_date + func.make_interval(0, 0, 0, Subscription.duration_month)
                < today,
            )
            .all()
        )

        for sub in expired_subs:
            user = sub.created_by
            expiration_date = sub.start_date + timedelta(days=30 * sub.duration_month)

            print(f"[NOTIFY] Subscription ID {sub.id} for user {user.username} is expired.")

            subject = "Your subscription has expired"
            body = render_template(
                "emails/subscription_expired.html",
                user=user,
                subscription=sub,
                expiration_date=expiration_date.strftime("%Y-%m-%d"),
            )
            send_and_log_email(user.email, subject, body)
