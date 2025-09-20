import logging
import re

from flask_appbuilder.security.sqla.models import User
from sqlalchemy import cast, func, or_
from sqlalchemy.dialects.postgresql import INTERVAL

from app import app, db, scheduler
from app.service_api.models.api_service_subscription_model import ApiServiceSubscription
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

        subscriptions = (
            db.session.query(ApiServiceSubscription)
            .filter(
                func.now()
                > (
                    ApiServiceSubscription.start_date
                    + cast(
                        func.concat(ApiServiceSubscription.duration_month, " month"),
                        INTERVAL,
                    )
                ),
                or_(
                    ApiServiceSubscription.is_upgrade == False,
                    ApiServiceSubscription.is_renew == False,
                ),
            )
            .all()
        )

        for sub in subscriptions:
            if sub.is_expired and sub.status == "active":
                user = sub.created_by
                if not user.id:
                    user = db.session.query(User).filter_by(username=user.username).first()
                    if not user or not user.id:
                        logger.error(f"User ID not found for subscription ID {sub.id}")
                        continue
                user_name = user.username
                slug_user_name = re.sub(r"[^a-zA-Z0-9]", "", user_name)
                service_slug = sub.service_plan.service.service_slug
                re.sub(r"[^a-zA-Z0-9]", "", sub.service_plan.plan.name.lower())
                # consumer_username = f"{service_slug}_{plan_name}_{slug_user_name}"
                consumer_username = f"{service_slug}_{slug_user_name}"
                if not user:
                    logger.warning(f"No user found for subscription ID {sub.id}")
                    continue

                apisix.delete_consumer(username=consumer_username)
                print(f"[CRON] Deleted consumer: {consumer_username}")

                # TODO add set sub.status to `inactive`

            else:
                print("[CRON] No expired subscriptions found.")
