# -*- coding: utf-8 -*-

import logging

from flask_appbuilder.api import BaseApi, ModelRestApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.service_plan_models import ServicePlan

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
]


class ServicePlanModelApi(ModelRestApi):
    resource_name = "service-plan"
    base_order = ("price", "asc")
    datamodel = SQLAInterface(ServicePlan)
    add_columns = _service_plan_value_display_columns
    list_columns = _service_plan_value_display_columns
    show_columns = _service_plan_value_display_columns
    edit_columns = _service_plan_value_display_columns


appbuilder.add_api(ServicePlanModelApi)


class ServicePlanRessourceModelApi(BaseApi):
    resource_name = "service-plan-ressource"

    @expose("/all", methods=["GET"])
    def get_all_ressource_plan(self):
        """
        ---
        get:
            summary: Get all service plans with type "ressource"
            description: Returns a list of all service plans of type "ressource", including options and provider.
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
            query = db.session.query(ServicePlan).filter(
                ServicePlan.service_plan_type == "ressource"
            )
            plans = query.all()

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
            for plan in plans:
                result.append(
                    {
                        "id": plan.id,
                        "price": plan.price,
                        "service_plan_type": plan.service_plan_type,
                        "preparation_time": plan.preparation_time,
                        "options": [serialize_option(opt) for opt in plan.options],
                        "provider_info": plan.provider_info,
                    }
                )

            return self.response(200, result=result)

        except Exception as e:
            return self.response(500, message=str(e))


appbuilder.add_api(ServicePlanRessourceModelApi)
