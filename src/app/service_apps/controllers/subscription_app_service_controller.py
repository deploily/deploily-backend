# -*- coding: utf-8 -*-

from flask import current_app, render_template
from flask_appbuilder.api import expose, protect
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import current_user, jwt_required

from app import appbuilder, db
from app.core.celery_tasks.send_mail_task import send_mail
from app.core.controllers.subscription_controllers import SubscriptionModelApi
from app.core.models.mail_models import Mail
from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)
from app.utils.utils import get_user

api_columns = [
    "application_status",
    "access_url",
    "required_restart",
    "deployment_error",
    "version",
    "demo_url",
    "console_url",
    "managed_ressource_details",
]

edit_columns = ["application_status"]


class AppServiceSubscriptionModelApi(SubscriptionModelApi):
    resource_name = "app-service-subscription"
    datamodel = SQLAInterface(SubscriptionAppService)

    add_columns = SubscriptionModelApi.add_columns + api_columns
    list_columns = SubscriptionModelApi.list_columns + api_columns
    show_columns = SubscriptionModelApi.show_columns + api_columns
    edit_columns = edit_columns

    @expose("/", methods=["GET"])
    @protect()  # or @jwt_required() depending on your setup
    @jwt_required()
    def get_list(self):
        """
        ---
        get:
          summary: Get active App Service Subscriptions
          description: >
            Returns a list of active (non-expired) app service subscriptions
            belonging to the current authenticated user.
          tags:
            - App Service Subscription
          security:
            - BearerAuth: []   # JWT authentication
          responses:
            "200":
              description: Successful response with valid subscriptions
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      result:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: integer
                              example: 12
                            name:
                              type: string
                              example: My Service
                            is_expired:
                              type: boolean
                              example: false
                            created_by:
                              type: string
                              example: user@test.com
            "401":
              description: Unauthorized (missing or invalid token)
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: Unauthorized
        """
        user = get_user()
        if not user:
            return self.response(401, message="Unauthorized")

        # Load all subscriptions for the current user
        all_items = (
            self.datamodel.session.query(self.datamodel.obj).filter_by(created_by=user).all()
        )

        # Filter out expired items (computed property)
        valid_items = [item for item in all_items if not item.is_expired]

        # Convert to dict for JSON response
        result = [item.to_dict() for item in valid_items]

        return self.response(200, result=result)

    def post_update(self, item):
        user = current_user
        notify_email = current_app.config.get("NOTIFICATION_EMAIL")

        # Check if a restart is required but hasn't been flagged yet
        if not item.required_restart and item.application_status in ["deployed", "error"]:
            item.required_restart = True
            db.session.commit()

        if item.required_restart and item.application_status == "processing":
            # Prepare email body using template
            email_body = render_template(
                "emails/restart_application.html",
                user=user,
                application=item.service_plan.service.name,
                subscription_id=item.id,
            )

            # Create and persist the email record
            email = Mail(
                title=f"Your application is restarting, {user.username}",
                body=email_body,
                email_to=notify_email,
                email_from=notify_email,
                mail_state="outGoing",
            )
            db.session.add(email)
            db.session.commit()

            # Send the email asynchronously
            send_mail.delay(email.id)

            print("### Email sent to:", notify_email)

            user_email_body = render_template(
                "emails/user_restart_application.html",
                user=user,
                application=item.service_plan.service.name,
                subscription_id=item.id,
            )

            # Create and persist the email record
            email = Mail(
                title=f"Your application is restarting, {user.username}",
                body=user_email_body,
                email_to=user.email,
                email_from=notify_email,
                mail_state="outGoing",
            )
            db.session.add(email)
            db.session.commit()

            # Send the email asynchronously
            send_mail.delay(email.id)

            print("### Email sent to:", notify_email)

            item.required_restart = False
            db.session.commit()

        return super().post_update(item)


appbuilder.add_api(AppServiceSubscriptionModelApi)
