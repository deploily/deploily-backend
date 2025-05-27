# -*- coding: utf-8 -*-

import logging

from flask import jsonify
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.security.sqla.models import Role, User

from app import appbuilder, db
from app.core.models.subscription_models import Subscription
from app.service_api.models.api_services_model import ApiService
from app.service_apps.models.apps_services_model import AppService
from app.service_cicd.models.cicd_services_model import CicdService
from app.service_ressources.models.services_ressources_providers_model import (
    ProvidersRessourceService,
)

_logger = logging.getLogger(__name__)


class StatisticsApi(BaseApi):
    resource_name = "statistics"

    @expose("/counts", methods=["GET"])
    def get_counts(self, **kwargs):
        """
        ---
        get:
          summary: Get system statistics
          description: Returns total number of services, subscriptions, users, and providers.
          responses:
            200:
              description: Statistics retrieved successfully
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      services:
                        type: integer
                        example: 10
                      subscriptions:
                        type: integer
                        example: 25
                      users:
                        type: integer
                        example: 100
                      providers:
                        type: integer
                        example: 5
            500:
              description: Internal server error
        """
        try:
            api_services_count = db.session.query(ApiService).count()
            app_services_count = db.session.query(AppService).count()
            ci_cd_services_count = db.session.query(CicdService).count()
            subscriptions_count = db.session.query(Subscription).count()
            users_count = (
                db.session.query(User).join(User.roles).filter(Role.name != "Admin").count()
            )
            providers_count = db.session.query(ProvidersRessourceService).count()

            return (
                jsonify(
                    {
                        "api_services": api_services_count,
                        "subscriptions": subscriptions_count,
                        "app_services": app_services_count,
                        "ci_cd_services": ci_cd_services_count,
                        "users": users_count,
                        "providers": providers_count,
                    }
                ),
                200,
            )

        except Exception as e:
            _logger.error(f"Error fetching statistics: {e}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500


appbuilder.add_api(StatisticsApi)
