# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_deployment.models.web_application_deployment_subscription_model import (
    WebApplicationSubscriptionDeploymentService,
)


class WebApplicationDeploymentServiceSubscriptionView(ModelView):
    datamodel = SQLAInterface(WebApplicationSubscriptionDeploymentService)

    list_columns = [
        "id",
        "created_by",
        "name",
        "byor",
        "start_date",
        "end_date",
        "is_expired",
        "status",
        "deployment_status",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    WebApplicationDeploymentServiceSubscriptionView,
    "Deployment web Application Subscriptions",
    icon="fa-cart-plus",
    category="Subscriptions",
)
