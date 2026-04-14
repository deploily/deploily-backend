import logging

from flask import jsonify, request
from flask_appbuilder.api import BaseApi, expose, protect
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from app import appbuilder, db
from app.core.models.rating_models import Score
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)


class RatingApi(BaseApi):
    resource_name = "rating"

    @protect()
    @jwt_required()
    @expose("/", methods=["POST"])
    def create_or_update_rating(self):
        """
        Create or update a rating for a service.
        ---
        post:
          description: Create or update a rating for a service.
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    service_id:
                      type: integer
                      example: 123
                    rating:
                      type: integer
                      example: 4
          responses:
            200:
              description: Rating created or updated
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                      id:
                        type: integer
            400:
              description: Bad input data
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      error:
                        type: string
        """
        data = request.get_json()
        user = get_user()

        if not data or "service_id" not in data or "rating" not in data:
            return jsonify({"error": "service_id and rating are required"}), 400

        service_id = data["service_id"]
        rating_value = data["rating"]

        try:
            rating = (
                db.session.query(Score).filter_by(service_id=service_id, created_by=user).first()
            )

            if rating:
                rating.rating = rating_value
                message = "Rating updated"
            else:
                rating = Score(service_id=service_id, rating=rating_value)
                rating.created_by = user
                db.session.add(rating)
                message = "Rating created"

            db.session.commit()
            return jsonify({"message": message, "id": rating.id}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            _logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Database error"}), 500


appbuilder.add_api(RatingApi)
