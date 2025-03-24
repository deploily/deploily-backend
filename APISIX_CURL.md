## APISIX Configuration

## Create service and upstream
```bash
curl -X POST "http://127.0.0.1:9180/apisix/admin/services" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "name": "flask-appbuilder-service",
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "localhost:5000": 1
    }
  }
}'
```
## Create route
```bash
curl -X POST "admin-api.deploily.cloud/routes/1" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "methods": ["GET", "POST"],
  "uri": "/api/*",
  "upstream_id": "00000000000000000070",
  "plugins": {
    "key-auth": {"consumer": "flask_consumer"}
  }
}'
```

## Create upstream
```bash
curl -X POST "http://127.0.0.1:9180/apisix/admin/upstreams" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "type": "roundrobin",
  "nodes": {
    "localhost:5000": 1
  }
}'
```

## Associate upstream with service
```bash
curl -X PUT "http://127.0.0.1:9180/apisix/admin/services/00000000000000000068" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "upstream_id": "00000000000000000070"
}'
```

## Create route
```bash
curl -X POST "http://127.0.0.1:9180/apisix/admin/routes/1" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "methods": ["GET", "POST"],
  "uri": "/api/*",
  "upstream_id": "00000000000000000070",
  "plugins": {
    "key-auth": {"consumer": "flask_consumer"}
  }
}'
```

## Create consumer
```bash
curl -X PUT "https://admin-api.deploily.cloud/apisix/admin/consumers/flask111111_consumer" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "username": "flask111111_consumer"
}'
```
## create a route with key-auth for a specific consumer
```bash
curl -X POST "http://127.0.0.1:9180/apisix/admin/routes" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "methods": ["GET", "POST"],
  "uri": "/api/*",
  "upstream_id": "00000000000000000020",
  "plugins": {
    "key-auth": {
      "consumer": "flask_consumer"
    }
  }
}'
```

## Get consumers list 

```bash
curl -X GET http://127.0.0.1:9180/apisix/admin/consumers -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"
```

## Get consumer details 

```bash
curl -X GET http://127.0.0.1:9180/apisix/admin/consumers/cart_2_user -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"
```

## Define Upstream Photon 

```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/upstreams/1 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "nodes": {
        "photon.ttk-test.xyz:443": 1
    },
    "type": "roundrobin",
    "scheme": "https",
    "pass_host": "rewrite",
    "upstream_host": "photon.ttk-test.xyz"
}'
```

## Define Service Photon
```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/services/1 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "photon-service",
    "upstream_id": "1",
    "plugins": {
        "proxy-rewrite": {
            "uri": "/api"
        },
        "key-auth": {}
    }
}'
```
##  Define Route Photon
```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/1 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "photon-route",
    "uri": "/photon*",
    "methods": ["GET"],
    "service_id": "1",
    "status": 1,
    "plugins": {
        "consumer-restriction": {
            "type": "whitelist",
            "whitelist": ["cart_line_2_user"]
        }
    }
}'

```
## Configuration Test

```bash
curl -H "apikey:  	 	0fdf370a2938b6dbb7defe0d5fd45e2" "https://api.deploily.cloud/photon?q=berlin"

```
curl -H "apikey:  	 	505cef9e08744559966a2028ab04bffd" "https://api.deploily.cloud/photon?q=berlin"

curl -H "apikey: KhIW+rKyEMFjT9Y6liNDOR6Ym9N9ycMwQw89JoJiq1QcRPO77W86dgpI2ReILi" "https://api.deploily.cloud/photon?q=berlin"
## Missing API key found in request
```bash
curl "https://api.deploily.cloud/photon?q=berlin"
```

## Invalid API key in request
```bash
curl -H "apikey: b2376542c6adbe480dc1ce0ca4acc852" "https://api.deploily.cloud/photon?q=berlin"
```
## Define ORS Upstream

```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/upstreams/2 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "nodes": {
        "ors.ttk-test.xyz:443": 1
    },
    "type": "roundrobin",
    "scheme": "https",
    "pass_host": "rewrite",
    "upstream_host": "ors.ttk-test.xyz"
}'
```

## Define ORS Service 
```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/services/2 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "ors-service",
    "upstream_id": "2",
    "plugins": {
        "proxy-rewrite": {
            "uri": "/ors/v2/matrix/driving-car"
        },
        "key-auth": {}
    }
}'
```

##  Define ORS Route
```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/2 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "ors-route",
    "uri": "/ors*",
    "methods": ["POST"],
    "service_id": "2",
    "status": 1,
    "plugins": {
        "consumer-restriction": {
            "type": "consumer_name",
            "whitelist": ["cart_line_1_user"]
        }
    }
}'
```
## Test ORS API

```bash
curl -d '{"locations":[[0.70093,35.477473],[3.207916,36.153868]], "sources":[0], "destinations":[1], "metrics":["distance", "duration"], "units":"km"}' \
-H "Content-Type: application/json" \
-H "apikey: b2376542c6adbe480dc1ce0ca4acc852" \
-X POST "https://api.deploily.cloud/ors"
```

## Define Nominatim Upstream  

```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/upstreams/3 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "nodes": {
        "nominatim.ttk-test.xyz:443": 1
    },
    "type": "roundrobin",
    "scheme": "https",
    "pass_host": "rewrite",
    "upstream_host": "nominatim.ttk-test.xyz"
}'
```

## Define Nominatim Service 

```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/services/3 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "nominatim-service",
    "upstream_id": "3",
    "plugins": {
        "proxy-rewrite": {
            "uri": "/reverse"
        },
        "key-auth": {}
    }
}'
```

##  Define Nominatim Route
```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/3 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "nominatim-route",
    "uris": ["/nominatim", "/nominatim/*"],
    "methods": ["GET", "POST"],
    "service_id": "3",
    "status": 1,
    "plugins": {
        "consumer-restriction": {
            "type": "consumer_name",
            "whitelist": ["cart_line_1_user"]
        }
    }
}'

```
## Test Nominatim API

```bash
curl -H "apikey: f456dd821ca840819fe44d5db9d14506" "https://api.deploily.cloud/nominatim?lat=35.30538822124727&lon=-1.1417971423748299&format=json&accept-language=fr"
```

## Define Wilaya Upstream

```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/upstreams/4 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "nodes": {
        "api-wilaya.ttk-test.xyz:443": 1
    },
    "type": "roundrobin",
    "scheme": "https",
    "pass_host": "rewrite",
    "upstream_host": "api-wilaya.ttk-test.xyz"
}'
```
## Define Wilaya Service 
```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/services/4 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "wilaya-service",
    "upstream_id": "4",
    "plugins": {
        "proxy-rewrite": {
            "uri": "/api/v1/getWilaya"
        },
        "key-auth": {}
    }
}'

```
##  Define Nominatim Route
```bash
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/4 \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
    "name": "wilaya-route",
    "uri": "/wilaya*",
    "methods": ["GET", "POST"],
    "service_id": "4",
    "status": 1,
    "plugins": {
        "consumer-restriction": {
            "type": "consumer_name",
            "whitelist": ["cart_line_1_user"]
        }
    }
}'
```
## Test Nominatim API

```bash
curl -H "apikey: 1b1bad9aefbe4002ba881a2113ab9cb" "https://api.deploily.cloud/wilaya?lat=35&long=0"
```


## Get upstreams
```bash
curl -X GET https://admin-api.deploily.cloud/apisix/admin/upstreams \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"
```
## Get services
```bash
curl -X GET https://admin-api.deploily.cloud/apisix/admin/services \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"
```
## Get routes
```bash
curl -X GET https://admin-api.deploily.cloud/apisix/admin/routes \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"
```
## Get consumers
```bash
curl -X GET https://admin-api.deploily.cloud/apisix/admin/consumers \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1"
```


