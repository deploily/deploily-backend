# -*- coding: utf-8 -*-


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.my_service_models import MyService


class MyServiceModelView(ModelView):
    route_base = "/admin/my-service"
    datamodel = SQLAInterface(MyService)
    list_columns = ["id", "start_date", "amount", "duration_month"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    MyServiceModelView,
    "My Service",
    icon="fa-solid fa-sliders",
    category="Service",
)
