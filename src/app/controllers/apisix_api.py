from flask import request, jsonify
from flask_appbuilder.api import BaseApi, expose
from app import appbuilder
from app.services.apisix_service import ApiSixService

class ApiSixController(BaseApi):
    resource_name = "apisix-controller"  

    @expose("/create-service", methods=["POST"])
    def create_service(self):
        """
        Create a new service in APIsix
        ---
        post:
          requestBody:
            content:
              application/json:
                schema:
                  properties:
                    service_name:
                      type: string
                      description: Name of the service
                      example: flask-appbuilder-service
                    upstream_nodes:
                      type: object
                      description: Upstream nodes for the service
                      additionalProperties:
                        type: integer
                      example: { "localhost:5000": 1 }
          responses:
            201:
              description: Service created successfully
            400:
              description: Invalid data
            500:
              description: Failed to create service
        """
 
        data = request.get_json()

      
        if not data or 'service_name' not in data or 'upstream_nodes' not in data:
            return self.response(400, message="Données invalides")
        
        service_name = data['service_name']
        upstream_nodes = data['upstream_nodes']
        
        # Appeler le service pour créer le service dans APISix
        api_service = ApiSixService(admin_url="http://127.0.0.1:9180/apisix/admin")
        service = api_service.create_service(service_name, upstream_nodes)
        
        if service:
            return self.response(201, message="Service créé avec succès", data=service)
        else:
            return self.response(500, message="Échec de la création du service")

appbuilder.add_api(ApiSixController)









