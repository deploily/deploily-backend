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
curl -X PUT "http://127.0.0.1:9180/apisix/admin/consumers/flask_consumer" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-H "Content-Type: application/json" \
-d '{
  "username": "flask_consumer",
  "plugins": {
    "key-auth": {
      "key": "my-api-key"
    }
  }
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

## Define Upstream

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

## Define Service 
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
##  Define Route
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
            "whitelist": ["cart_line_1_user"]
        }
    }
}'

```

## Configuration Test

```bash
curl -H "apikey: b2376542c6adbe480dc1ce0ca4acc852" "https://api.deploily.cloud/photon?q=berlin"

```
## Missing API key found in request
```bash
curl "https://api.deploily.cloud/photon?q=berlin"
```

## Invalid API key in request
```bash
curl -H "apikey: b2376542c6adbe480dc1ce0ca4acc852" "https://api.deploily.cloud/photon?q=berlin"
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


