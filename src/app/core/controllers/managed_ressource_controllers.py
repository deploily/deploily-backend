import logging

from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.core.models.managed_ressource_models import ManagedRessource
from app.core.models.service_plan_models import ServicePlan
from app.core.models.subscription_models import Subscription
from app.service_ressources.models.services_ressources_category_model import (
    ServiceRessouceCategory,
)
from app.service_ressources.models.services_ressources_model import RessourceService
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

display_columns = [
    "id",
    "ip",
    "host_name",
    "operator_system",
    "subscriptions",
    "ressource_service_plan",
    "time_remaining",
]


class ManagedRessourceModelApi(BaseApi):
    resource_name = "managed-ressource"

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

            ressource_service_ids = [
                r[0]
                for r in (
                    db.session.query(RessourceService.id)
                    .join(RessourceService.ressouce_category)
                    .filter(
                        RessourceService.type == "ressource_service",
                        ServiceRessouceCategory.category_type == "vps",
                    )
                    .all()
                )
            ]

            # Get plan IDs that belong to those services
            ressource_plan_ids = [
                r[0]
                for r in (
                    db.session.query(ServicePlan.id)
                    .filter(ServicePlan.service_id.in_(ressource_service_ids))
                    .all()
                )
            ]

            managed_ressources = (
                db.session.query(ManagedRessource)
                .join(ManagedRessource.subscriptions)
                .filter(
                    ManagedRessource.ressource_service_plan_id.in_(ressource_plan_ids),
                    Subscription.created_by.has(id=user.id),
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
                        "provider_name": service_plan.provider_info,
                        "host_name": res.host_name,
                        "ip": res.ip,
                        "start_date": res.start_date,
                        "end_date": res.end_date,
                    }
                )

            return self.response(200, result=result)

        except Exception as e:
            return self.response(500, message=str(e))

    @expose("/web-hosting", methods=["GET"])
    @protect()
    @jwt_required()
    def get_managed_ressource_web_hosting(self):
        """
        ---
        get:
            summary: Get managed ressources web hosting  of the current user
            description: Returns a list of managed ressources  and their service plans for the logged-in user.
            responses:
                200:
                    description: A list of managed ressources web hosting
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

            ressource_service_ids = [
                r[0]
                for r in (
                    db.session.query(RessourceService.id)
                    .join(RessourceService.ressouce_category)
                    .filter(
                        RessourceService.type == "ressource_service",
                        ServiceRessouceCategory.category_type == "web_hosting",
                    )
                    .all()
                )
            ]

            # Get plan IDs that belong to those services
            ressource_plan_ids = [
                r[0]
                for r in (
                    db.session.query(ServicePlan.id)
                    .filter(ServicePlan.service_id.in_(ressource_service_ids))
                    .all()
                )
            ]

            managed_ressources = (
                db.session.query(ManagedRessource)
                .join(ManagedRessource.subscriptions)
                .filter(
                    ManagedRessource.ressource_service_plan_id.in_(ressource_plan_ids),
                    Subscription.created_by.has(id=user.id),
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
                        "provider_name": service_plan.provider_info,
                        "host_name": res.host_name,
                        "dns": res.dns,
                        "ip": res.ip,
                        "start_date": res.start_date,
                        "end_date": res.end_date,
                    }
                )
            print(result)

            return self.response(200, result=result)

        except Exception as e:
            return self.response(500, message=str(e))

    @expose("/dns", methods=["GET"])
    @protect()
    @jwt_required()
    def get_managed_ressource_dns(self):
        """
        ---
        get:
            summary: Get managed ressources dns  of the current user
            description: Returns a list of managed ressources  and their service plans for the logged-in user.
            responses:
                200:
                    description: A list of managed ressources dns
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

            ressource_service_ids = [
                r[0]
                for r in (
                    db.session.query(RessourceService.id)
                    .join(RessourceService.ressouce_category)
                    .filter(
                        RessourceService.type == "ressource_service",
                        ServiceRessouceCategory.category_type == "dns",
                    )
                    .all()
                )
            ]

            # Get plan IDs that belong to those services
            ressource_plan_ids = [
                r[0]
                for r in (
                    db.session.query(ServicePlan.id)
                    .filter(ServicePlan.service_id.in_(ressource_service_ids))
                    .all()
                )
            ]

            managed_ressources = (
                db.session.query(ManagedRessource)
                .join(ManagedRessource.subscriptions)
                .filter(
                    ManagedRessource.ressource_service_plan_id.in_(ressource_plan_ids),
                    Subscription.created_by.has(id=user.id),
                )
                .all()
            )

            if not managed_ressources:
                return self.response(200, result=[])

            # Step 2: Get the ServicePlans linked to those managed ressources
            result = []
            for res in managed_ressources:
                service_plan = res.ressource_service_plan
                if not service_plan:

                    continue

                result.append(
                    {
                        "id": service_plan.id,
                        "managed_ressource_id": res.id,
                        "plan_name": service_plan.plan.name if service_plan.plan else None,
                        "service_name": service_plan.service.name if service_plan.service else None,
                        "provider_name": service_plan.provider_info,
                        "host_name": res.host_name,
                        "dns": res.dns,
                        "start_date": res.start_date,
                        "end_date": res.end_date,
                    }
                )
            print(result)

            return self.response(200, result=result)

        except Exception as e:
            return self.response(500, message=str(e))


appbuilder.add_api(ManagedRessourceModelApi)
