# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
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
    "ttk_epay_email_from",
    "ttk_epay_email_host",
    "ttk_epay_email_smtp_server",
    "ttk_epay_email_port",
    "ttk_epay_email_username",
    "ttk_epay_email_password",
    "ttk_epay_recaptcha_secret_key",
    "ttk_epay_recaptcha_site_key",
    "ttk_epay_address",
    "ttk_epay_commercial_register",
    "ttk_epay_tax_article",
    "ttk_epay_nif",
    "ttk_epay_nis",
]


class TtkEpayAppServiceSubscriptionModelApi(AppServiceSubscriptionModelApi):

    resource_name = "ttk-epay-app-service-subscription"
    datamodel = SQLAInterface(TtkEpaySubscriptionAppService)

    add_columns = AppServiceSubscriptionModelApi.add_columns + api_columns
    list_columns = AppServiceSubscriptionModelApi.list_columns + api_columns
    show_columns = AppServiceSubscriptionModelApi.show_columns + api_columns
    edit_columns = AppServiceSubscriptionModelApi.edit_columns + api_columns


appbuilder.add_api(TtkEpayAppServiceSubscriptionModelApi)
