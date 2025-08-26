# -*- coding: utf-8 -*-

import logging

from flask import request
from flask_appbuilder.api import BaseApi, ModelRestApi, expose
from flask_appbuilder.models.sqla.filters import FilterEqual
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import and_
from sqlalchemy.orm import aliased

from app import appbuilder, db
from app.core.models.service_plan_models import ServicePlan
from app.core.models.service_plan_option_models import ServicePlanOption
from app.service_apps.models.apps_services_model import AppService
from app.service_ressources.models.services_ressources_category_model import (
    ServiceRessouceCategory,
)
from app.service_ressources.models.services_ressources_model import RessourceService

_logger = logging.getLogger(__name__)

_service_plan_value_display_columns = [
    "id",
    "price",
    "service_id",
    "service",
    "subscription_category",
    "plan",
    "options",
    "is_custom",
    "service_plan_type",
    "provider_info",
    "preparation_time",
    "unity",
]


class ServicePlanModelApi(ModelRestApi):
    resource_name = "service-plan"
    base_order = ("price", "asc")
    datamodel = SQLAInterface(ServicePlan)
    add_columns = _service_plan_value_display_columns
    list_columns = _service_plan_value_display_columns
    show_columns = _service_plan_value_display_columns
    edit_columns = _service_plan_value_display_columns

    base_filters = [["is_published", FilterEqual, True]]


appbuilder.add_api(ServicePlanModelApi)


class ServicePlanRessourceModelApi(BaseApi):
    resource_name = "service-plan-ressource-vps"

    @expose("/all", methods=["GET"])
    def get_all_ressource_plan(self):
        """
        ---
        get:
            summary: Get all service plans with type "ressource"
            description: Returns a list of all service plans of type "ressource", including options and provider.
            parameters:
                - in: query
                  name: app_service_id
                  required: true
                  schema:
                    type: integer
                  description: id of the selected app
                - in: query
                  name: subscription_category
                  required: false
                  schema:
                    type: string
                  description: category of subscription (yearly/montly)

            responses:
                200:
                    description: A list of service plans
                    content:
                        application/json:
                            schema:
                                type: array
                                items:
                                    type: object
                500:
                    description: Internal server error
        """
        try:
            app_service_id = request.args.get("app_service_id")
            subscription_category = (
                request.args.get("subscription_category")
                if request.args.get("subscription_category")
                else "yearly"
            )
            cpu_option = aliased(ServicePlanOption)
            ram_option = aliased(ServicePlanOption)
            disk_option = aliased(ServicePlanOption)
            ressources_services = (
                db.session.query(RessourceService)
                .join(RessourceService.ressouce_category)
                .filter(
                    RessourceService.type == "ressource_service",
                    RessourceService.is_published.is_(True),
                    ServiceRessouceCategory.category_type == "vps",
                )
                .all()
            )
            if not ressources_services:
                return self.response(200, result=[])
            query = (
                db.session.query(ServicePlan)
                .join(AppService, AppService.id == ServicePlan.service_id)
                .join(cpu_option, ServicePlan.options)
                .join(ram_option, ServicePlan.options)
                .join(disk_option, ServicePlan.options)
                .filter(ServicePlan.display_on_app.is_(True))
                .filter(ServicePlan.is_custom.is_(False))
                .filter(ServicePlan.subscription_category == subscription_category)
                .filter(cpu_option.option_type == "cpu")
                .filter(ram_option.option_type == "ram")
                .filter(disk_option.option_type == "disque")
                .order_by(ServicePlan.price.asc(), ServicePlan.priority.asc())
            )

            if app_service_id:
                query = query.filter(
                    and_(
                        ServicePlan.service_id == app_service_id,
                        AppService.minimal_cpu <= cpu_option.option_value,
                        AppService.minimal_ram <= ram_option.option_value,
                        AppService.minimal_disk <= disk_option.option_value,
                    )
                )

            vps_ressources_plans = query.all()

            if not vps_ressources_plans:
                return self.response(200, result=[])

            def serialize_option(option):
                return {
                    "id": option.id,
                    "option_type": option.option_type,
                    "option_value": option.option_value,
                    "icon": option.icon,
                    "html_content": option.html_content,
                    "sequence": option.sequence,
                }

            result = []
            for plan in vps_ressources_plans:
                result.append(
                    {
                        "id": plan.id,
                        "plan_name": plan.plan.name,
                        "service_name": plan.service.name,
                        "service_id": plan.service.id,
                        "price": plan.price,
                        "service_plan_type": plan.service_plan_type,
                        "preparation_time": plan.preparation_time,
                        "subscription_category": plan.subscription_category,
                        "unity": plan.unity,
                        "options": [serialize_option(opt) for opt in plan.options],
                        "provider_info": plan.provider_info,
                    }
                )

            return self.response(200, result=result)

        except Exception as e:
            return self.response(500, message=str(e))


appbuilder.add_api(ServicePlanRessourceModelApi)
