# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.promo_usage_models import PromoUsage


class PromoUsageModelView(ModelView):
    route_base = "/admin/promo-usage"
    datamodel = SQLAInterface(PromoUsage)
    list_columns = ["id", "user_id", "promo_code_id", "used_at"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    PromoUsageModelView,
    "Promo Usage",
    icon="fa-solid fa-sliders",
    category="Promo Code",
)
