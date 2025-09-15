# -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.service_apps.controllers.subscription_app_service_controller import (
    AppServiceSubscriptionModelApi,
)
from app.service_apps.models.hi_events_subscription_model import (
    HiEventSubscriptionAppService,
)

api_columns = [
    "event_url",
    "event_domain",
]
from app import appbuilder


class HiEventsAppServiceSubscriptionModelApi(AppServiceSubscriptionModelApi):

    resource_name = "hi-events-app-service-subscription"
    datamodel = SQLAInterface(HiEventSubscriptionAppService)

    add_columns = AppServiceSubscriptionModelApi.add_columns + api_columns
    list_columns = AppServiceSubscriptionModelApi.list_columns + api_columns
    show_columns = AppServiceSubscriptionModelApi.show_columns + api_columns
    edit_columns = AppServiceSubscriptionModelApi.edit_columns + api_columns


appbuilder.add_api(HiEventsAppServiceSubscriptionModelApi)
