# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.service_apps.models.odoo_subscription_model import OdooSubscriptionAppService


class OdooAppServiceSubscriptionView(ModelView):
    datamodel = SQLAInterface(OdooSubscriptionAppService)

    list_columns = [
        "id",
        "created_by",
        "byor",
        "ressource_service_plan",
        "start_date",
        "end_date",
        "is_expired",
        "status",
        "is_upgrade",
        "is_renew",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on", "type"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


appbuilder.add_view(
    OdooAppServiceSubscriptionView,
    "App Odoo Subscriptions",
    icon="fa-shopping-bag",
    category="Subscriptions",
)
