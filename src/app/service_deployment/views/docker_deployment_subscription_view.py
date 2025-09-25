# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_deployment.models.docker_deployment_subscription_model import (
    DockerSubscriptionDeploymentService,
)


class DockerDeploymentServiceSubscriptionView(ModelView):
    datamodel = SQLAInterface(DockerSubscriptionDeploymentService)

    list_columns = [
        "id",
        "created_by",
        "price",
        "total_amount",
        "status",
        "is_expired",
        "start_date",
        "duration_month",
        "is_upgrade",
        "is_renew",
        "description",
        "deployment_status",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    DockerDeploymentServiceSubscriptionView,
    "Docker Deployment Subscription",
    icon="fa-cog",
    category="Deployments",
)
