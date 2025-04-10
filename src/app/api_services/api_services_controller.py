# from flask import jsonify
# from flask_appbuilder.api import expose, protect
# from flask_jwt_extended import jwt_required

# from app import appbuilder
# from app.controllers.consumer_controllers import ConsumerApi


# class CustomConsumerApi(ConsumerApi):

#     @protect()
#     @jwt_required()
#     @expose("/<int:subscribe_id>/inhereted", methods=["POST"])
#     def create_custom_consumer(self, subscribe_id):
#         """
#         Crée un consommateur personnalisé pour un service donné.

#         ---
#         post:
#           description: Crée un consommateur personnalisé et génère une clé API.
#           parameters:
#             - in: path
#               name: subscribe_id
#               required: true
#               schema:
#                 type: integer
#               description: ID du service auquel associer le consommateur.
#           responses:
#             200:
#               description: Consommateur créé avec succès.
#               content:
#                 application/json:
#                   schema:
#                     type: object
#                     properties:
#                       message:
#                         type: string
#                         example: "Custom consumer created successfully"
#                       api_key:
#                         type: string
#                         example: "123456abcdef"
#             400:
#               description: Erreur - service non trouvé.
#             500:
#               description: Erreur interne du serveur.
#         """
#         response, status_code = super().create_my_service_consumer(subscribe_id)

#         if isinstance(response, dict):
#             data = response
#         else:
#             try:
#                 data = response.get_json()
#             except AttributeError:
#                 return jsonify({"error": "Invalid response format"}), 500

#         if "auth-key" not in data or not data["auth-key"]:
#             return jsonify({"error": "API key generation failed"}), 500

#         return (
#             jsonify(
#                 {"message": "Custom consumer created successfully", "auth-key": data["auth-key"]}
#             ),
#             200,
#         )


# appbuilder.add_api(CustomConsumerApi)
