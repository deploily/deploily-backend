# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_deployment.models.deployment_service_subscription_model import (
    SubscriptionDeploymentService,
)


class SubscriptionDeploymentServiceView(ModelView):
    datamodel = SQLAInterface(SubscriptionDeploymentService)

    list_columns = [
        "id",
        "created_by",
        "price",
        "total_amount",
        "status",
        "is_expired",
        "start_date",
        "duration_month",
        "access_url",
        "service_name",
        "required_restart",
        "deployment_status",
        "is_published",
    ]

    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns
    base_permissions = ["can_list", "can_show"]  # only allow viewing


appbuilder.add_view(
    SubscriptionDeploymentServiceView,
    "Subscription Deployment Services",
    icon="fa-cogs",
    category="Deployments",
)
