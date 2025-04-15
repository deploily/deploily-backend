# -*- coding: utf-8 -*-

import logging
import os
import uuid

from flask import jsonify, request
from flask_appbuilder import expose
from flask_appbuilder.api import ModelRestApi, protect
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app import appbuilder, db
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
    "payment_receipt",
]


class PaymentModelApi(ModelRestApi):
    resource_name = "payments"
    base_order = ("id", "desc")
    exclude_route_methods = "delete"
    datamodel = SQLAInterface(Payment)
    add_columns = _payment_display_columns
    list_columns = _payment_display_columns
    edit_columns = _payment_display_columns

    @protect()
    @jwt_required()
    @expose("/<int:payment_id>/upload-receipt", methods=["POST"])
    def upload_receipt(self, payment_id):
        """
        Upload receipt for a payment
        ---
        post:
          description: Upload a receipt file for a specific payment.
          parameters:
            - in: path
              name: payment_id
              required: true
              schema:
                type: integer
              description: ID of the payment
          requestBody:
            required: true
            content:
              multipart/form-data:
                schema:
                  type: object
                  properties:
                    receipt:
                      type: string
                      format: binary
                      description: Receipt file to upload
          responses:
            200:
              description: Receipt uploaded successfully
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: Receipt uploaded successfully
            400:
              description: Missing or invalid receipt file
            404:
              description: Payment not found
            500:
              description: Internal server error
        """
        try:
            file = request.files.get("receipt")
            if not file or file.filename == "":
                return jsonify({"error": "Receipt file is required"}), 400

            payment = db.session.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                return jsonify({"error": "Payment not found"}), 404

            extension = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{extension}"
            filename = secure_filename(filename)
            relative_folder = "uploads"
            absolute_folder = os.path.join(appbuilder.app.static_folder, relative_folder)
            os.makedirs(absolute_folder, exist_ok=True)

            file_path = os.path.join(absolute_folder, filename)
            file.save(file_path)

            payment.payment_receipt = filename
            db.session.commit()

            return jsonify({"message": "Receipt uploaded successfully"}), 200

        except Exception:
            _logger.exception("Error while uploading receipt")
            return jsonify({"error": "Unexpected error occurred"}), 500


appbuilder.add_api(PaymentModelApi)
