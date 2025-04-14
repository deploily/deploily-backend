# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.payment_profile_models import PaymentProfile


class PaymentProfileModelView(ModelView):
    route_base = "/admin/profile"
    datamodel = SQLAInterface(PaymentProfile)
    list_columns = [
        "id",
        "name",
        "profile_type",
        "user_id",
        "phone",
        "company_name",
        "company_registration_number",
        "is_default_profile",
        "is_company",
    ]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    PaymentProfileModelView,
    "Payment profile",
    icon="fa-solid fa-sliders",
    category="Billing",
)
