import logging

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

        subscriptions = db.session.query(Subscription).all()
        for sub in subscriptions:
            if sub.is_expired:
                deleted_usernames = set()

                user = sub.created_by

                if not user:
                    logger.warning(f"No user found for subscription ID {sub.id}")
                    continue

                consumer_username = user.username

                if consumer_username in deleted_usernames:
                    continue

                apisix.delete_consumer(username=consumer_username)
                print(f"[CRON] Deleted consumer: {consumer_username}")
                deleted_usernames.add(consumer_username)

            else:
                print("[CRON] No expired subscriptions found.")
