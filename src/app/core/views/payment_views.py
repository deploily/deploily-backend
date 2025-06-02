# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.payment_models import Payment


class PaymentModelView(ModelView):
    route_base = "/admin/payment"
    datamodel = SQLAInterface(Payment)
    list_columns = [
        "id",
        "created_by",
        "amount",
        "payment_method",
        "status",
        "profile",
        "start_date",
    ]
    base_order = ("id", "desc")
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns


db.create_all()
appbuilder.add_view(
    PaymentModelView,
    "Payments",
    icon="fa-solid fa-sliders",
    category="Billing",
)
