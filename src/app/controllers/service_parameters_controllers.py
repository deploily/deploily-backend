import logging
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.service_parameters_models import ServiceParameters

_logger = logging.getLogger(__name__)


class ServiceParametersModelApi(ModelRestApi):
    resource_name = "serviceParameters"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(ServiceParameters)

appbuilder.add_api(ServiceParametersModelApi)