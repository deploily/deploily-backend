import logging
import re

from flask_appbuilder.security.sqla.models import User
from sqlalchemy import and_, cast, func
from sqlalchemy.dialects.postgresql import INTERVAL

from app import app, db, scheduler
from app.service_api.models.api_service_subscription_model import ApiServiceSubscription
from app.services.apisix_service import ApiSixService

logger = logging.getLogger(__name__)


@scheduler.task("cron", id="delete_consumer", max_instances=1, hour=0, minute=0)
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
                # Check if the subscription is expired based on start_date + duration_month
                func.now()
                > (
                    ApiServiceSubscription.start_date
                    + cast(
                        func.concat(ApiServiceSubscription.duration_month, " month"),
                        INTERVAL,
                    )
                ),
                # Only consider active subscriptions that are not upgrades or renewals or already expired or have status active
                and_(
                    ApiServiceSubscription.is_upgrade == False,
                    ApiServiceSubscription.is_renew == False,
                    ApiServiceSubscription.is_expired == True,
                    ApiServiceSubscription.status == "active",
                ),
            )
            .all()
        )

        for sub in subscriptions:
            print(
                f"[CRON] Processing subscription: {sub.id} - is_expired: {sub.is_expired} and status: {sub.status}"
            )
            user = sub.created_by
            if not user.id:
                user = db.session.query(User).filter_by(username=user.username).first()
                if not user or not user.id:
                    logger.error(f"User ID not found for subscription ID {sub.id}")
                    continue

            # Compute consumer username
            user_name = user.username
            slug_user_name = re.sub(r"[^a-zA-Z0-9]", "", user_name)
            service_slug = sub.service_plan.service.service_slug
            consumer_username = f"{service_slug}_{slug_user_name}"

            if not user:
                logger.warning(f"No user found for subscription ID {sub.id}")
                continue

            apisix.delete_consumer(username=consumer_username)
            print(f"[CRON] Deleted consumer: {consumer_username}")

            sub.status = "inactive"
            db.session.commit()
            print(f"[CRON] Updated subscription status to inactive for subscription ID {sub.id}")
