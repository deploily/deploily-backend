from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.service_parameter_models import ServiceParameter


class ServiceParameterModelView(ModelView):
    route_base = "/admin/service-parameter"
    datamodel = SQLAInterface(ServiceParameter)

    list_columns = [
        "id",
        "icon",
        "html_content",
        "service_plans",
        "option_type",
        "option_value",
    ]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    ServiceParameterModelView,
    "Service Parameter",
    icon="fa-solid fa-check-circle-o",
    category="Master",
)
