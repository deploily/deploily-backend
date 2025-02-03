# -*- coding: utf-8 -*-


# TODO 5


# TODO post_update 
# TODO create Service + Route + Upstream + ...


from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app import db
from app.models.a6service_models import A6Service


class A6ServiceModelView(ModelView):
    route_base = "/admin/A6Service"
    datamodel = SQLAInterface(A6Service)
    list_columns = ["id", "name","cart"]
    base_order = ("id", "desc")

    add_columns = ["name","cart"]
    edit_columns = ["name","cart"]
    show_columns = ["id", "name", "cart"]

    def post_update(self, item):
        """
        Cette méthode est appelée après la mise à jour d'un service.
        """
    

db.create_all()
appbuilder.add_view(
    A6ServiceModelView,
    "A6Service",
    icon="fa-solid fa-cogs",
    category="A6Service",
)
