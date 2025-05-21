import logging

from sqlalchemy import func

from app import app, db, scheduler
from app.core.models import Subscription
from app.services.apisix_service import ApiSixService

logger = logging.getLogger(__name__)


@scheduler.task("cron", id="delete_consumer", max_instances=1, minute="*/1")
def delete_expired_consumers():
    print(">>> [CRON] delete_expired_consumers() running")
    with app.app_context():
        print("[CRON] Starting expired consumer cleanup...")

        try:
            apisix = ApiSixService()
        except Exception as e:
            print(f"Cannot initialize APISIX client: {e}")
            return

        expired_subs = (
            db.session.query(Subscription)
            .filter(
                func.DATE(
                    Subscription.start_date + func.make_interval(0, Subscription.duration_month)
                )
                < func.now()
            )
            .all()
        )

        if not expired_subs:
            print("[CRON] No expired subscriptions found.")
            return

        deleted_usernames = set()

        for sub in expired_subs:
            user = sub.created_by

            if not user:
                logger.warning(f"No user found for subscription ID {sub.id}")
                continue

            consumer_username = user.username

            if consumer_username in deleted_usernames:
                continue

            try:
                apisix.delete_consumer(username=consumer_username)
                print(f"[CRON] Deleted consumer: {consumer_username}")
                deleted_usernames.add(consumer_username)
            except Exception as e:
                print(f"Failed to delete consumer {consumer_username}: {e}")
