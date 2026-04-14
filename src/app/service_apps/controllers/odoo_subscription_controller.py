# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.service_apps.controllers.subscription_app_service_controller import (
    AppServiceSubscriptionModelApi,
)
from app.service_apps.models.odoo_subscription_model import OdooSubscriptionAppService

api_columns = [
    "odoo_password",
]
from app import appbuilder


class OdooAppServiceSubscriptionModelApi(AppServiceSubscriptionModelApi):

    resource_name = "odoo-app-service-subscription"
    datamodel = SQLAInterface(OdooSubscriptionAppService)

    add_columns = AppServiceSubscriptionModelApi.add_columns + api_columns
    list_columns = AppServiceSubscriptionModelApi.list_columns + api_columns
    show_columns = AppServiceSubscriptionModelApi.show_columns + api_columns
    edit_columns = AppServiceSubscriptionModelApi.edit_columns + api_columns


appbuilder.add_api(OdooAppServiceSubscriptionModelApi)
