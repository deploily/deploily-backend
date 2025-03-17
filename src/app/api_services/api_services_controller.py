from flask import jsonify
from flask_appbuilder.api import expose
from flask_jwt_extended import jwt_required
from app import appbuilder
from app.controllers.consumer_controllers import ConsumerApi


class CustomConsumerApi(ConsumerApi):
    resource_name = "custom-my-service"
    @expose("/<int:my_service_id>/custom-consumer", methods=["POST"])
    def create_custom_consumer(self, my_service_id):
        """
        Crée un consommateur personnalisé pour un service donné.

        ---
        post:
          description: Crée un consommateur personnalisé et génère une clé API.
          parameters:
            - in: path
              name: my_service_id
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
        response, status_code = self.create_my_service_consumer(my_service_id)  

        print(f"DEBUG: Response = {response}, Status = {status_code}")


        if isinstance(response, dict):
            data = response
        else:
            try:
                data = response.get_json()
            except AttributeError:
                return jsonify({"error": "Invalid response format"}), 500  

        data["message"] = "Custom consumer created successfully"

        return jsonify(data), status_code


appbuilder.add_api(CustomConsumerApi)
