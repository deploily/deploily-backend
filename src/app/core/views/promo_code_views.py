# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.promo_code_models import PromoCode


class PromoCodeModelView(ModelView):
    route_base = "/admin/promo-code"
    datamodel = SQLAInterface(PromoCode)
    list_columns = ["id", "code", "rate", "expiration_date", "active", "usage_type", "is_valid"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    PromoCodeModelView,
    "Promo Code",
    icon="fa-solid fa-sliders",
    category="Billing",
)
