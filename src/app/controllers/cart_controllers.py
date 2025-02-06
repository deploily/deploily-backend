import logging
import secrets
from flask_appbuilder.api import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models.cart_models import Cart
from app.services.apisix_service import ApiSixService  

# TODO 2 

# TODO Add modelRestAPI for Order

# TODO post_update ==> create consumer

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
        Called after updating a cart to change its status and create a consumer
        """
        if cart.status == "done":
            
            consumer_username = f"cart_{cart.id}_user"
            
       
            api_key = secrets.token_hex(16)  
            
            
            apisix_service = ApiSixService()  
            response = apisix_service.create_consumer(consumer_username, api_key)
            
            if response:
                _logger.info(f"Consumer créé avec succès : {consumer_username}")
            else:
                _logger.error(f"Échec de la création du consumer pour le panier {cart.id}")

            db.session.commit()



appbuilder.add_api(CartModelApi)