import logging

from flask_appbuilder.api import ModelRestApi, expose, protect
from flask_appbuilder.models.sqla.filters import BaseFilter
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import jwt_required
from sqlalchemy import exists

from app import appbuilder, db
from app.core.models.managed_ressource_models import ManagedRessource
from app.core.models.subscription_models import Subscription
from app.service_ressources.models.services_ressources_category_model import (
    ServiceRessouceCategory,
)
from app.service_ressources.models.services_ressources_model import RessourceService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

display_columns = [
    "id",
    "ressource_service_plan",
    "start_date",
    "end_date",
    "ressource_type",
    "service_details",
    "time_remaining",
    "service_details",
]


# ✅ Custom filter that uses a proper EXISTS subquery
class FilterBySubscriptionOwner(BaseFilter):
    def apply(self, query, value):
        current_user = get_user()
        return query.filter(
            exists().where(
                (Subscription.managed_ressource_id == ManagedRessource.id)
                & (Subscription.created_by == current_user)
            )
        )


class ManagedRessourceModelApi(ModelRestApi):
    resource_name = "managed-ressource"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ManagedRessource)

    # ✅ Use the custom filter, no value needed (None is the trigger value)
    base_filters = [["id", FilterBySubscriptionOwner, lambda: None]]

    exclude_route_methods = ("put", "post", "delete", "info", "get")
    add_columns = display_columns
    list_columns = display_columns
    edit_columns = display_columns
    _exclude_columns = [
        "changed_on",
        "created_by",
        "changed_by",
    ]

    @expose("/vps", methods=["GET"])
    @protect()
    @jwt_required()
    def get_managed_ressource_vps(self):
        """
        ---
        get:
            summary: Get managed ressources of the current user
            description: Returns a list of managed ressources and their service plans for the logged-in user.
            responses:
                200:
                    description: A list of managed ressources
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
            user = get_user()
            if not user:
                return self.response(401, message="Unauthorized")

            # Step 1: Get all ManagedRessource linked to this user's subscriptions
            user = get_user()

            managed_ressources = (
                db.session.query(ManagedRessource)
                .join(Subscription, ManagedRessource.subscriptions)
                .filter(Subscription.created_by.has(id=user.id))
                .all()
            )
            managed_ressources = (
                db.session.query(ManagedRessource)
                .join(ManagedRessource.subscriptions)
                .join(ManagedRessource.ressource_service_plan)
                .join(RessourceService.ressouce_category)
                .filter(
                    Subscription.created_by.has(id=user.id),
                    RessourceService.is_published.is_(True),
                    ServiceRessouceCategory.category_type == "vps",
                )
                .all()
            )

            if not managed_ressources:
                return self.response(200, result=[])

            # Step 2: Get the ServicePlans linked to those managed ressources
            result = []
            for res in managed_ressources:
                service_plan = res.ressource_service_plan
                if not service_plan or not service_plan.display_on_app or service_plan.is_custom:
                    continue

                result.append(
                    {
                        "id": service_plan.id,
                        "managed_ressource_id": res.id,
                        "plan_name": service_plan.plan.name if service_plan.plan else None,
                        "service_name": service_plan.service.name if service_plan.service else None,
                        "service_id": service_plan.service.id if service_plan.service else None,
                        "price": service_plan.price,
                        "service_plan_type": service_plan.service_plan_type,
                        "preparation_time": service_plan.preparation_time,
                        "unity": service_plan.unity,
                        "time_remaining": res.time_remaining,
                        "options": [
                            {
                                "id": opt.id,
                                "option_type": opt.option_type,
                                "option_value": opt.option_value,
                                "icon": opt.icon,
                                "html_content": opt.html_content,
                                "sequence": opt.sequence,
                            }
                            for opt in service_plan.options
                        ],
                        "provider_info": service_plan.provider_info,
                        "subscription_ids": [sub.id for sub in res.subscriptions],
                    }
                )

            return self.response(200, result=result)

        except Exception as e:
            return self.response(500, message=str(e))


appbuilder.add_api(ManagedRessourceModelApi)
