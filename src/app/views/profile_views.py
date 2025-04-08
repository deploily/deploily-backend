# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.models.profile_models import Profile


class ProfileModelView(ModelView):
    route_base = "/admin/profile"
    datamodel = SQLAInterface(Profile)
    list_columns = [
        "id",
        "name",
        "profile_type",
        "user_id",
        "phone",
        "company_name",
        "company_registration_number",
    ]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ProfileModelView,
    "Payment profile",
    icon="fa-solid fa-sliders",
    category="Billing",
)
