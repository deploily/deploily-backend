# -*- coding: utf-8 -*-

import logging

from flask import Response, jsonify, request
from flask_appbuilder.api import ModelRestApi, expose, protect
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import jwt_required

from app import appbuilder, db
from app.models.my_favorites_models import MyFavorites
from app.models.service_models import Service
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class MyFavoritesModelApi(ModelRestApi):
    resource_name = "my-favorites"
    base_order = ("id", "desc")
    datamodel = SQLAInterface(MyFavorites)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    exclude_route_methods = "post"

    add_columns = ["id", "service_id"]
    list_columns = ["id", "service", "created_on", "created_by.id"]
    edit_columns = ["id", "service_id"]
    _exclude_columns = ["changed_by", "changed_on", "created_by"]

    @protect()
    @jwt_required()
    @expose("/service", methods=["POST"])
    def add_remove_favorite(self):
        """
        If service_id and created_by_fk exist, delete the record.
        Otherwise, add a new record to MyFavorites.
        ---
        post:
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    service_id:
                      type: integer
                      description: Service ID
          responses:
            200:
              description: OK
            400:
              description: Bad request
            404:
              description: Service not found
            500:
              description: Internal server error
        """

        data = request.get_json()
        service_id = data.get("service_id")
        user = get_user()
        user_id = user.id

        if not service_id or not user_id:
            return Response("Both service_id and user_id are required", status=400)

        service = db.session.query(Service).filter_by(id=service_id).first()
        if not service:
            return Response("Service not found", status=404)

        try:
            my_favorite = (
                db.session.query(MyFavorites)
                .filter_by(service_id=service_id, created_by_fk=user.id)
                .first()
            )

            if my_favorite:
                db.session.delete(my_favorite)
                db.session.commit()
                return jsonify({"message": "Favorite successfully removed"}), 200
            else:
                new_favorite = MyFavorites(service_id=service_id, created_by_fk=user.id)
                db.session.add(new_favorite)
                db.session.commit()
                return jsonify({"message": "Favorite successfully added"}), 200

        except Exception as e:
            db.session.rollback()
            _logger.error(f"Error while managing the favorite: {e}")
            return Response("Internal server error", status=500)


appbuilder.add_api(MyFavoritesModelApi)
