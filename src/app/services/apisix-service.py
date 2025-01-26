# -- coding: utf-8 --
import requests
import json

class ApiSixService:
    def __init__(self, admin_url="http://127.0.0.1:9180/apisix/admin"):
        # URL de l'API Admin d'APIsix
        self.admin_url = admin_url
    
    def create_service(self, service_name, upstream_nodes):
        # Définir les données du service à créer
        service_data = {
            "name": service_name,
            "upstream": {
                "type": "roundrobin",
                "nodes": upstream_nodes
            }
        }
        
        # Spécifiez les en-têtes pour la requête
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": "edd1c9f034335f136f87ad84b625c8f1" 
        }
        
        # Effectuer la requête POST pour créer le service
        try:
            response = requests.post(f"{self.admin_url}/services", 
                                     data=json.dumps(service_data), 
                                     headers=headers)
            
            # Vérifier la réponse de l'API
            if response.status_code == 201:
                print("Service créé avec succès !")
                return response.json()
            else:
                print(f"Échec de la création du service: {response.status_code}, {response.text}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            return None

if __name__ == "__main__":
    # Initialiser l'objet ApiSixService
    api_service = ApiSixService(admin_url="http://127.0.0.1:9180/apisix/admin")  
    
   
    service_name = "flask-appbuilder-service"  
    upstream_nodes = {
        "localhost:5000": 1  
    }
    
    service = api_service.create_service(service_name, upstream_nodes)
    
    if service:
        print("Service créé avec les détails suivants :")
        print(service)
