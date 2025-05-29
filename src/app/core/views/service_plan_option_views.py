from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.service_plan_option_models import ServicePlanOption


class ServicePlanOptionModelView(ModelView):
    route_base = "/admin/service-plan-option"
    datamodel = SQLAInterface(ServicePlanOption)

    list_columns = [
        "id",
        "icon",
        "html_content",
        "service_plan_id",
        "option_type",
        "option_value",
    ]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ServicePlanOptionModelView,
    "Service Plan Option",
    icon="fa-solid fa-cogs",
    category="Master",
)
