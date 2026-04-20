# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_ressources.models.subscription_ressource_service_model import (
    SubscriptionRessourceService,
)


class SubscriptionRessourceServiceView(ModelView):
    datamodel = SQLAInterface(SubscriptionRessourceService)

    list_columns = [
        "id",
        "created_by",
        "service_name",
        "byor",
        "start_date",
        "end_date",
        "total_amount",
        "status",
        "application_status",
        "required_restart",
    ]

    base_order = ("id", "desc")
    _exclude_columns = [
        "created_on",
        "changed_on",
        "type",
    ]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    SubscriptionRessourceServiceView,
    "Ressource Services Subscriptions",
    icon="fas fa-luggage-cart",
    category="Subscriptions",
)
