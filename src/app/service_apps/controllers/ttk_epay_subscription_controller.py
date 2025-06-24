# -*- coding: utf-8 -*-

from flask import current_app, render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import current_user

from app import appbuilder, db
from app.core.celery_tasks.send_mail_task import send_mail
from app.core.models.mail_models import Mail
from app.service_apps.controllers.subscription_app_service_controller import (
    AppServiceSubscriptionModelApi,
)
from app.service_apps.models.ttk_epay_subscription_model import (
    TtkEpaySubscriptionAppService,
)

api_columns = [
    "ttk_epay_api_secret_key",
    "ttk_epay_client_site_url",
    "ttk_epay_client_site_name",
    "ttk_epay_client_site_logo_url",
    "ttk_epay_client_site_privacy",
    "ttk_epay_client_site_terms",
    "ttk_epay_client_site_phone_number",
    "ttk_epay_client_site_address",
    "ttk_epay_client_site_email",
    "ttk_epay_satim_server_url",
    "ttk_epay_satim_base_url",
    "ttk_epay_satim_fail_url",
    "ttk_epay_satim_confirm_url",
    "ttk_epay_satim_client_server_url",
    "ttk_epay_satim_user_name",
    "ttk_epay_satim_password",
    "ttk_epay_satim_terminal_id",
    "ttk_epay_satim_language",
    "ttk_epay_satim_description",
    "ttk_epay_satim_currency",
    "ttk_epay_satim_json_params",
    "ttk_epay_mvc_satim_server_url",
    "ttk_epay_mvc_satim_fail_url",
    "ttk_epay_mvc_satim_confirm_url",
]


class TtkEpayAppServiceSubscriptionModelApi(AppServiceSubscriptionModelApi):

    resource_name = "ttk-epay-app-service-subscription"
    datamodel = SQLAInterface(TtkEpaySubscriptionAppService)

    add_columns = AppServiceSubscriptionModelApi.add_columns + api_columns
    list_columns = AppServiceSubscriptionModelApi.list_columns + api_columns
    show_columns = AppServiceSubscriptionModelApi.show_columns + api_columns
    edit_columns = AppServiceSubscriptionModelApi.edit_columns + api_columns

    def post_update(self, item):
        user = current_user
        notify_email = current_app.config.get("NOTIFICATION_EMAIL")

        # Check if a restart is required but hasn't been flagged yet
        if not item.required_restart and item.application_status == "deployed":
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


appbuilder.add_api(TtkEpayAppServiceSubscriptionModelApi)
