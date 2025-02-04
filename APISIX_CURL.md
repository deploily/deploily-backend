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