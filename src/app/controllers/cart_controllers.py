

# TODO 2 

# TODO Add modelRestAPI for Order

# TODO post_update ==> create consumer ....

from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.cart_models import Cart
import logging

_logger = logging.getLogger(__name__)

class CartModelApi(ModelRestApi):
    resource_name = "cart"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Cart)
    _exclude_columns = [
        "status",
    ]
    edit_exclude_columns = _exclude_columns

    def post_update(self, cart: Cart) -> None:
        """
        Called after updating an cart to change its status and create a consumer
        """
        if cart.status == "done":


            db.session.commit()


appbuilder.add_api(CartModelApi)
