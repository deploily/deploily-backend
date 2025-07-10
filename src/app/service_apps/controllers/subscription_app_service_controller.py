# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.core.controllers.subscription_controllers import SubscriptionModelApi
from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)

api_columns = [
    "application_status",
    "access_url",
    "required_restart",
    "deployment_error",
    "version",
    "demo_url",
    "console_url",
]

edit_columns = ["application_status"]


class AppServiceSubscriptionModelApi(SubscriptionModelApi):
    resource_name = "app-service-subscription"
    datamodel = SQLAInterface(SubscriptionAppService)

    add_columns = SubscriptionModelApi.add_columns + api_columns
    list_columns = SubscriptionModelApi.list_columns + api_columns
    show_columns = SubscriptionModelApi.show_columns + api_columns
    edit_columns = edit_columns


appbuilder.add_api(AppServiceSubscriptionModelApi)
