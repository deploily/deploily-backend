import logging
from datetime import datetime, timedelta

from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from app import appbuilder, db
from app.core.models.my_favorites_models import MyFavorites
from app.core.models.subscription_models import Subscription
from app.core.models.support_ticket_models import SupportTicket
from app.service_api.models.api_service_subscription_model import ApiServiceSubscription
from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)
from app.service_deployment.models.deployment_service_subscription_model import (
    SubscriptionDeploymentService,
)
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class DashboardApi(BaseApi):
    resource_name = "dashboard"

    openapi_spec_tag = "Dashboard"

    @protect()
    @jwt_required()
    @expose("/", methods=["GET"])
    def dashboard(self):
        """Dashboard
        ---
        get:
          summary: Get dashboard data
          description: Returns subscriptions expiring within 30 days
          tags:
            - Dashboard
          security:
            - jwt: []
          responses:
            200:
              description: Dashboard data
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      data:
                        type: object
                        properties:
                          expiring_soon:
                            type: array
                            items:
                              type: integer
                            description: List of subscription IDs expiring soon
                          count:
                            type: integer
                            description: Number of subscriptions expiring soon
            401:
              $ref: '#/components/responses/401'
            500:
              $ref: '#/components/responses/500'
        """
        user = get_user()
        now = datetime.now()
        in_30_days = now + timedelta(days=30)

        expiry_date = func.make_interval(0, Subscription.duration_month) + Subscription.start_date

        subscriptions_expiring_soon = (
            db.session.query(Subscription)
            .filter(
                Subscription.created_by.has(id=user.id),
                expiry_date >= now,
                expiry_date <= in_30_days,
            )
            .all()
        )
        api_subscriptions = (
            db.session.query(ApiServiceSubscription)
            .filter(ApiServiceSubscription.created_by.has(id=user.id))
            .count()
        )
        app_subscriptions = (
            db.session.query(SubscriptionAppService)
            .filter(SubscriptionAppService.created_by.has(id=user.id))
            .count()
        )
        deployment_subscriptions = (
            db.session.query(SubscriptionDeploymentService)
            .filter(SubscriptionDeploymentService.created_by.has(id=user.id))
            .count()
        )
        support_tickets = (
            db.session.query(SupportTicket).filter(SupportTicket.created_by.has(id=user.id)).count()
        )
        my_favorites = (
            db.session.query(MyFavorites).filter(MyFavorites.created_by.has(id=user.id)).count()
        )

        return self.response(
            200,
            data={
                "expiring_soon": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "service_plan": s.service_plan.service.name,
                        "start_date": s.start_date.isoformat(),
                        "duration_month": s.duration_month,
                        "expiry_date": (
                            s.start_date + timedelta(days=30 * s.duration_month)
                        ).isoformat(),
                        "status": s.status,
                        "payment_status": s.payment_status,
                        "price": s.price,
                        "total_amount": s.total_amount,
                    }
                    for s in subscriptions_expiring_soon
                ],
                "api_subscriptions": api_subscriptions,
                "app_subscriptions": app_subscriptions,
                "deployment_subscriptions": deployment_subscriptions,
                "support_tickets": support_tickets,
                "my_favorites": my_favorites,
            },
        )


appbuilder.add_api(DashboardApi)
