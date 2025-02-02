

# TODO 2 

# TODO Add modelRestAPI for Order

# TODO post_update ==> create consumer ....

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.order_models import Order
import logging

_logger = logging.getLogger(__name__)

class OrderModelApi(ModelRestApi):
    resource_name = "order"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Order)

    def post_update(self, order: Order) -> None:
        """
        Called after updating an order to change its status and create a consumer
        """
        if order.status == "draft":
            _logger.info(f"[ORDER API] Updating status for order {order.id}")
            order.status = "done"

            db.session.commit()


appbuilder.add_api(OrderModelApi)
