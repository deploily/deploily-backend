from flask import jsonify
from flask_appbuilder.api import expose

from app import appbuilder
from app.controllers.consumer_controllers import ConsumerApi


class CustomConsumerApi(ConsumerApi):
    resource_name = "custom-my-service"

    @expose("/<int:subscribe_id>/custom-consumer", methods=["POST"])
    def create_custom_consumer(self, subscribe_id):
        """
        Crée un consommateur personnalisé pour un service donné.

        ---
        post:
          description: Crée un consommateur personnalisé et génère une clé API.
          parameters:
            - in: path
              name: subscribe_id
              required: true
              schema:
                type: integer
              description: ID du service auquel associer le consommateur.
          responses:
            200:
              description: Consommateur créé avec succès.
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: "Custom consumer created successfully"
                      api_key:
                        type: string
                        example: "123456abcdef"
            400:
              description: Erreur - service non trouvé.
            500:
              description: Erreur interne du serveur.
        """
        response, status_code = super().create_my_service_consumer(subscribe_id)

        if isinstance(response, dict):
            data = response
        else:
            try:
                data = response.get_json()
            except AttributeError:
                return jsonify({"error": "Invalid response format"}), 500

        data["auth-key"] = "Hello World"
        return jsonify(data), status_code


appbuilder.add_api(CustomConsumerApi)
