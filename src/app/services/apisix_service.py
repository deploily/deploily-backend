# apisix_service.py
import requests
import json

# https://github.com/api7/python-sdk

# TODO  6

# TODO Replace requets with A6Client 

class ApiSixService:
    def __init__(self):
        # TODO move URLS to .env -> config -> get from config[]
        self.admin_url ="http://127.0.0.1:9180/apisix/admin"

        # self.client = A6Client()
    
    def create_service(self, service_name, upstream_nodes):
        service_data = {
            "name": service_name,
            "upstream": {
                "type": "roundrobin",
                "nodes": upstream_nodes
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": "edd1c9f034335f136f87ad84b625c8f1" 
        }
        
        try:
            response = requests.post(f"{self.admin_url}/services", 
                                     data=json.dumps(service_data), 
                                     headers=headers)
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Échec de la création du service: {response.status_code}, {response.text}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            return None
        
    def create_route(self, route_data):
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": "edd1c9f034335f136f87ad84b625c8f1" 
        }
        
        try:
            response = requests.post(f"{self.admin_url}/routes", 
                                     data=json.dumps(route_data), 
                                     headers=headers)
            
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Échec de la création de la route: {response.status_code}, {response.text}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
            return None
