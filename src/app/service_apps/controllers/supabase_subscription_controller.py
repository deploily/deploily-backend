# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.service_apps.controllers.subscription_app_service_controller import (
    AppServiceSubscriptionModelApi,
)
from app.service_apps.models.supabase_subscription_model import (
    SupabaseSubscriptionAppService,
)

api_columns = [
    "supabase_url",
    "supabase_anonKey",
]


class SupabaseAppServiceSubscriptionModelApi(AppServiceSubscriptionModelApi):

    resource_name = "supabse-app-service-subscription"
    datamodel = SQLAInterface(SupabaseSubscriptionAppService)

    add_columns = AppServiceSubscriptionModelApi.add_columns + api_columns
    list_columns = AppServiceSubscriptionModelApi.list_columns + api_columns
    show_columns = AppServiceSubscriptionModelApi.show_columns + api_columns
    edit_columns = AppServiceSubscriptionModelApi.edit_columns + api_columns
