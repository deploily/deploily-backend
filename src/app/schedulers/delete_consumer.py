import logging
import re
from sqlalchemy import text
from app import app, db, scheduler
from app.core.models import Subscription
from app.services.apisix_service import ApiSixService
from flask_appbuilder.security.sqla.models import User
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

        subscriptions = db.session.query(Subscription).filter(
            text("start_date + (duration_month || ' month')::interval < now()")
        ).all()

        for sub in subscriptions:
            if sub.is_expired:
                user = sub.created_by
                if not user.id:
                    user = db.session.query(User).filter_by(
                        username=user.username).first()
                    if not user or not user.id:
                        logger.error(
                            f"User ID not found for subscription ID {sub.id}")
                        continue
                user_name = user.username
                slug_user_name = re.sub(
                    r"[^a-zA-Z0-9]", "", user_name)
                service_slug = sub.service_plan.service.service_slug
                plan_name = re.sub(r"[^a-zA-Z0-9]", "",
                                   sub.service_plan.plan.name.lower())
                consumer_username = f"{service_slug}_{plan_name}_{slug_user_name}"
                if not user:
                    logger.warning(
                        f"No user found for subscription ID {sub.id}")
                    continue

                apisix.delete_consumer(username=consumer_username)
                print(f"[CRON] Deleted consumer: {consumer_username}")

            else:
                print("[CRON] No expired subscriptions found.")
