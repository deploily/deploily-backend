import logging
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.service_models import Service

_logger = logging.getLogger(__name__)

class ServiceModelApi(ModelRestApi):
    resource_name = "service"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Service)

appbuilder.add_api(ServiceModelApi)