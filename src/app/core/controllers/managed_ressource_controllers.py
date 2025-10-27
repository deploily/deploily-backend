import logging

from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.core.models.managed_ressource_models import ManagedRessource
from app.core.models.subscription_models import Subscription
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

    @expose("/", methods=["GET"])
    @protect()
    @jwt_required()
    def get_managed_ressource(self):
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

    # def pre_get_list(self, filters):
    #     print("pre_get_list called with filters:", filters)

    # @expose('/', methods=["GET"])
    # @has_access_api
    # def get_list(self):
    #     user = get_user()

    #     query = self.datamodel.session.query(ManagedRessource).join(ManagedRessource.subscriptions)
    #     print(f"User: {user}")
    #     print(f"###################################Query: {query}")

    #     # Assume one subscription per resource
    #     query = query.filter(ManagedRessource.subscriptions.any(created_by=user))
    #     print(f"Filtered Query--------------------------------------: {query}")

    #     # Pagination
    #     page = request.args.get("page", 1, type=int)
    #     page_size = request.args.get("page_size", self.page_size, type=int)
    #     count = query.count()

    #     results = query.offset((page - 1) * page_size).limit(page_size).all()
    #       # Marshal the results
    #     items = [self.response_model.dump(item) for item in results]

    #     # Return a standard response
    #     return jsonify({
    #         "count": count,
    #         "page": page,
    #         "page_size": page_size,
    #         "result": items,
    #         "ids": [item["id"] for item in items],
    #     })


appbuilder.add_api(ManagedRessourceModelApi)
