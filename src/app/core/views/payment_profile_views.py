# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.payment_profile_models import PaymentProfile


class PaymentProfileModelView(ModelView):
    route_base = "/admin/profile"
    datamodel = SQLAInterface(PaymentProfile)
    list_columns = [
        "id",
        "created_by",
        "name",
        "profile_type",
        "balance",
        "nin",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    PaymentProfileModelView,
    "Payment profile",
    icon="fa-solid fa-sliders",
    category="Billing",
)
