# -*- coding: utf-8 -*-

import logging
import os
import uuid

from flask import jsonify, request
from flask_appbuilder import expose
from flask_appbuilder.api import ModelRestApi, protect
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from app import appbuilder, db
from app.core.models.payment_models import Payment
from app.utils.utils import get_user

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
    exclude_route_methods = ["delete"]
    datamodel = SQLAInterface(Payment)
    add_columns = _payment_display_columns
    list_columns = _payment_display_columns
    edit_columns = _payment_display_columns
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    _exclude_columns = ["changed_by", "changed_on", "created_by"]

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
            413:
              description: File too large
            500:
              description: Internal server error
        """
        try:
            MAX_FILE_SIZE_KB = 500
            MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_KB * 1024

            file = request.files.get("receipt")
            if not file or file.filename == "":
                return jsonify({"error": "Receipt file is required."}), 400

            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0)

            if file_length > MAX_FILE_SIZE_BYTES:
                return (
                    jsonify(
                        {
                            "error": f"The file is too large. Maximum allowed size is {MAX_FILE_SIZE_KB}KB."
                        }
                    ),
                    413,
                )

            payment = db.session.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                return jsonify({"error": "Payment not found."}), 404

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

            return jsonify({"message": "Receipt uploaded successfully."}), 200

        except Exception:
            _logger.exception("Error while uploading receipt")
            return jsonify({"error": "An unexpected error occurred."}), 500


appbuilder.add_api(PaymentModelApi)
