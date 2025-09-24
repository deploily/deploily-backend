# # -*- coding: utf-8 -*-

# from flask_appbuilder.models.sqla.interface import SQLAInterface

# from app import appbuilder
# from app.service_deployment.controllers.subscription_deployment_service_controller import (
#     DeploymentServiceSubscriptionModelApi
# )
# from app.service_deployment.models.docker_deployment_subscription_model import (
#     DockerSubscriptionDeploymentService,
# )
# api_columns = [
#     ]

# class DockerDeploymentServiceSubscriptionModelApi(DeploymentServiceSubscriptionModelApi):

#     resource_name = "deployment-app-service-subscription"
#     datamodel = SQLAInterface(DeploymentServiceSubscriptionModelApi)

#     add_columns = DeploymentServiceSubscriptionModelApi.add_columns + api_columns
#     list_columns = DeploymentServiceSubscriptionModelApi.list_columns + api_columns
#     show_columns = DeploymentServiceSubscriptionModelApi.show_columns + api_columns
#     edit_columns = DeploymentServiceSubscriptionModelApi.edit_columns + api_columns


# appbuilder.add_api(DeploymentServiceSubscriptionModelApi)
