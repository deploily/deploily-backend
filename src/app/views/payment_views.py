# -*- coding: utf-8 -*-
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.payment_models import Payment


class PaymentModelView(ModelView):
    route_base = "/admin/payment"
    datamodel = SQLAInterface(Payment)
    list_columns = ["id", "amount", "payment_method",
                    "subscription_id", "status"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    PaymentModelView,
    "Parameters Value",
    icon="fa-solid fa-sliders",
    category="Payment",
)
