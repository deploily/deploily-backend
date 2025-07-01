# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.promo_code.models.api_tokens_model import ApiToken


class ApiTokensModelView(ModelView):
    route_base = "/admin/api-tokens"
    datamodel = SQLAInterface(ApiToken)
    list_columns = ["id", "partner", "token", "rate"]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ApiTokensModelView,
    "Api Tokens",
    icon="fa-solid fa-cogs",
    category="Billing",
)
