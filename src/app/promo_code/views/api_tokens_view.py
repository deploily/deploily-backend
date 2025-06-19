# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.promo_code.models.api_tokens_model import ApiToken


class ApiTokensModelView(ModelView):
    route_base = "/admin/api-tokens"
    datamodel = SQLAInterface(ApiToken)
    list_columns = ["id", "token"]
    _exclude_columns = ["created_on", "changed_on"]
    add_exclude_columns = _exclude_columns
    edit_exclude_columns = _exclude_columns
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ApiTokensModelView,
    "Aoi Tokens",
    icon="fa-solid fa-cogs",
    category="Billing",
)
