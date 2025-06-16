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
    "api_secret_key",
    "client_site_url",
    "client_site_name",
    "client_site_logo_url",
    "client_site_privacy",
    "client_site_terms",
    "client_site_phone_number",
    "client_site_address",
    "client_site_email",
    "satim_server_url",
    "satim_base_url",
    "satim_fail_url",
    "satim_confirm_url",
    "satim_client_server_url",
    "satim_user_name",
    "satim_password",
    "satim_terminal_id",
    "satim_language",
    "satim_description",
    "satim_currency",
    "satim_json_params",
    "mvc_satim_server_url",
    "mvc_satim_fail_url",
]


class TtkEpayAppServiceSubscriptionModelApi(AppServiceSubscriptionModelApi):

    resource_name = "ttk-epay-app-service-subscription"
    datamodel = SQLAInterface(TtkEpaySubscriptionAppService)

    add_columns = AppServiceSubscriptionModelApi.add_columns + api_columns
    list_columns = AppServiceSubscriptionModelApi.list_columns + api_columns
    show_columns = AppServiceSubscriptionModelApi.show_columns + api_columns
    edit_columns = AppServiceSubscriptionModelApi.edit_columns + api_columns


appbuilder.add_api(TtkEpayAppServiceSubscriptionModelApi)
