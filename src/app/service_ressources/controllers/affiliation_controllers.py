# -*- coding: utf-8 -*-

import logging

from flask import current_app, jsonify, render_template, request
from flask_appbuilder.api import ModelRestApi, expose, protect
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_jwt_extended import current_user, jwt_required

from app import appbuilder, db
from app.core.models.service_plan_models import ServicePlan
from app.service_ressources.models.affiliation_model import Affiliation
from app.service_ressources.models.services_ressources_model import RessourceService
from app.services.mail_service import send_and_log_email
from app.utils.utils import get_user

_logger = logging.getLogger(__name__)

_affiliation_value_display_columns = [
    "id",
    "total_price",
    "affiliation_state",
    "provider",
    "service_plan",
]


class AffiliationModelApi(ModelRestApi):
    resource_name = "affiliation"
    datamodel = SQLAInterface(Affiliation)
    base_filters = [["created_by", FilterEqualFunction, get_user]]
    exclude_route_methods = ["get", "post", "get_list"]
    add_columns = _affiliation_value_display_columns
    list_columns = _affiliation_value_display_columns
    show_columns = _affiliation_value_display_columns
    edit_columns = _affiliation_value_display_columns

    @protect()
    @jwt_required()
    @expose("/create", methods=["POST"])
    def create_affiliation(self):
        """
        Create a new affiliation for a service plan.
        ---
        post:
          summary: Create affiliation to a provider service plan
          description: Creates a new affiliation between the authenticated user and the selected service plan.
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  type: object
                  required:
                    - service_plan_selected_id
                    - total_price
                  properties:
                    service_plan_selected_id:
                      type: integer
                      description: ID of the selected service plan
                    total_price:
                      type: number
                      format: float
                      description: Total price of the affiliation
                    phone_number:
                      type: string
                      description: number of user

          responses:
            201:
              description: Affiliation created and emails sent
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: Affiliation created and emails sent
            400:
              description: Bad request (missing or invalid parameters)
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      error:
                        type: string
                      message:
                        type: string
            404:
              description: Resource not found (e.g. service plan or provider not found)
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      error:
                        type: string
            500:
              description: Internal server error
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      error:
                        type: string
        """
        data = request.get_json()
        service_plan_id = data.get("service_plan_selected_id")
        total_price = data.get("total_price")
        phone_number = data.get("phone_number")

        if not service_plan_id or total_price is None:
            return self.response_400(message="Missing required parameters.")

        service_plan = db.session.get(ServicePlan, service_plan_id)
        if not service_plan:
            return self.response_404(message="Service Plan not found.")

        ressource_service = (
            db.session.query(RessourceService).filter_by(id=service_plan.service_id).first()
        )
        if not ressource_service:
            return self.response_404(message="Associated RessourceService not found.")

        provider = ressource_service.provider
        if not provider:
            return self.response_404(message="Provider not found.")

        affiliation = Affiliation(
            service_plan_id=service_plan.id,
            provider_id=provider.id,
            phone_number=phone_number,
            total_price=total_price,
            affiliation_state="pending",
        )
        db.session.add(affiliation)
        db.session.commit()

        user = current_user
        print(
            f"ressource_service.name: {ressource_service.name}, service_plan.plan.name: {service_plan.plan.name}"
        )

        # -------- Email templates --------
        # Email to user
        user_email_body = render_template(
            "emails/user_affiliation.html",
            user=user,
            provider=provider,
            total_price=total_price,
        )
        send_and_log_email(
            to=user.email,
            subject=f"Nouvelle affiliation dans deploily.cloud",
            body=user_email_body,
        )

        # Email to internal team
        deploily_email_body = render_template(
            "emails/deploily_affiliation.html",
            user=user,
            provider=provider,
            total_price=total_price,
        )
        send_and_log_email(
            to=current_app.config["NOTIFICATION_EMAIL"],
            subject=f"New affiliation between the user {user.first_name} and the provider {provider.name}",
            body=deploily_email_body,
        )

        return self.response(201, message="Affiliation créée et emails envoyés.")

    @protect()
    @jwt_required()
    @expose("/all", methods=["GET"])
    def get_all_affiliations(self):
        """
        Get all affiliations with details.
        ---
        get:
          summary: List all affiliations
          description: Returns a list of all affiliations with service and provider details.
          responses:
            200:
              description: A list of affiliations
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        service_name:
                          type: string
                        provider_name:
                          type: string
                        total_price:
                          type: number
                        affiliation_state:
                          type: string
                        created_on:
                          type: string
                          format: date-time
            401:
              description: Unauthorized - JWT token missing or invalid
            500:
              description: Internal server error
        """
        user = current_user
        affiliations = db.session.query(Affiliation).filter_by(created_by=user).all()
        results = []
        for affiliation in affiliations:
            result = {
                "id": affiliation.id,
                "service_name": (
                    affiliation.service_plan.service.name
                    if affiliation.service_plan and affiliation.service_plan.service
                    else None
                ),
                "provider_name": affiliation.provider.name if affiliation.provider else None,
                "total_price": affiliation.total_price,
                "affiliation_state": affiliation.affiliation_state,
                "created_on": affiliation.created_on if affiliation.created_on else None,
            }
            results.append(result)

        return jsonify(results), 200


appbuilder.add_api(AffiliationModelApi)
