# -*- coding: utf-8 -*-

import logging

from flask import jsonify
from flask_appbuilder.api import ModelRestApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from requests import Session

from app import appbuilder
from app.models.payment_models import Payment

_logger = logging.getLogger(__name__)
_payment_display_columns = [
    "id",
    "amount",
    "status",
    "start_date",
    "payment_method",
    "subscription_id",
    "profile_id",
    "subscription",
    "profile",
]


class PaymentModelApi(ModelRestApi):
    resource_name = "payment"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(Payment)
    add_columns = _payment_display_columns
    list_columns = _payment_display_columns
    edit_columns = _payment_display_columns

    @expose("/delete_all", methods=["DELETE"])
    def delete_all(self):
        """
        Supprime tous les paiements enregistrés dans la base de données.

        ---
        delete:
          description: Supprime toutes les entrées de la table Payment.
          responses:
            200:
              description: Succès - Retourne le nombre de paiements supprimés.
              content:
                application/json:
                  example:
                    message: "100 payments deleted successfully"
            500:
              description: Erreur interne du serveur.
              content:
                application/json:
                  example:
                    error: "An error occurred while deleting payments"
        """
        try:
            session: Session = self.datamodel.session
            num_deleted = session.query(Payment).delete()
            session.commit()
            return jsonify({"message": f"{num_deleted} payments deleted successfully"}), 200
        except Exception as e:
            session.rollback()
            _logger.error(f"Error deleting all payments: {str(e)}")
            return jsonify({"error": "An error occurred while deleting payments"}), 500


appbuilder.add_api(PaymentModelApi)
