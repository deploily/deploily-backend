# # -*- coding: utf-8 -*-

from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_deployment.controllers.subscription_deployment_service_controller import (
    DeploymentServiceSubscriptionModelApi,
)
from app.service_deployment.models.mobile_application_deployment_subscription_model import (
    MobileApplicationSubscriptionDeploymentService,
)

docker_service_columns = []


class MobileApplicationDeploymentServiceSubscriptionModelApi(DeploymentServiceSubscriptionModelApi):

    resource_name = "mobile-application-deployment-service-subscription"
    datamodel = SQLAInterface(MobileApplicationSubscriptionDeploymentService)

    add_columns = DeploymentServiceSubscriptionModelApi.add_columns + docker_service_columns
    list_columns = DeploymentServiceSubscriptionModelApi.list_columns + docker_service_columns
    show_columns = DeploymentServiceSubscriptionModelApi.show_columns + docker_service_columns
    edit_columns = DeploymentServiceSubscriptionModelApi.edit_columns + docker_service_columns


appbuilder.add_api(MobileApplicationDeploymentServiceSubscriptionModelApi)
