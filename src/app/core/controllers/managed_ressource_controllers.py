import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.filters import BaseFilter
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import exists

from app import appbuilder
from app.core.models.managed_ressource_models import ManagedRessource
from app.core.models.subscription_models import Subscription
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

display_columns = [
    "id",
    "ressource_service_plan",
    "start_date",
    "end_date",
    "ressource_type",
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


appbuilder.add_api(ManagedRessourceModelApi)
