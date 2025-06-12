# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from slugify import slugify

from app import appbuilder, db
from app.service_apps.models.ttk_epay_subscription_model import (
    TtkEpaySubscriptionAppService,
)


class TtkEpatSubscriptionAppServiceView(ModelView):
    datamodel = SQLAInterface(TtkEpaySubscriptionAppService)

    list_columns = [
        "id",
        "created_by",
        "price",
        "total_amount",
        "status",
        "is_expired",
        "start_date",
        "duration_month",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns

    def post_add(self, item):
        item.service_slug = slugify(item.name)
        db.session.commit()


appbuilder.add_view(
    TtkEpatSubscriptionAppServiceView,
    "Subscription TTK Epay ",
    icon="fa-cogs",
    category="Application Subscription Services",
)
