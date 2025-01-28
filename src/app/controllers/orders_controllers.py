

# TODO 2 

# TODO Add modelRestAPI for Order

# TODO post_update ==> create consumer ....

import logging

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder
from app.models.order_models import Order

_logger = logging.getLogger(__name__)

class OrderModelApi(ModelRestApi):
    resource_name = "order"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Order)

appbuilder.add_api(OrderModelApi)