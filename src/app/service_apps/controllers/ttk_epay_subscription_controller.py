# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_apps.controllers.subscription_app_service_controller import (
    SubscriptionAppServiceModelApi,
)
from app.service_apps.models.ttk_epay_subscription_model import (
    TtkEpaySubscriptionAppService,
)

api_columns = ["api_secret_key"]


class TtkEpaySubscriptionAppServiceModelApi(SubscriptionAppServiceModelApi):

    resource_name = "ttk-epay-subscription-app-service"
    datamodel = SQLAInterface(TtkEpaySubscriptionAppService)

    add_columns = SubscriptionAppServiceModelApi.add_columns + api_columns
    list_columns = SubscriptionAppServiceModelApi.list_columns + api_columns
    show_columns = SubscriptionAppServiceModelApi.show_columns + api_columns
    edit_columns = SubscriptionAppServiceModelApi.edit_columns + api_columns


appbuilder.add_api(TtkEpaySubscriptionAppServiceModelApi)
