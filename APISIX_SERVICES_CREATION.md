## Photon

```

curl -X PUT https://admin-api.deploily.cloud/apisix/admin/upstreams/photon-upstream \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
 -d '{
"type": "roundrobin",
"scheme": "https",
"pass_host": "rewrite",
"upstream_host": "photon.ttk-test.xyz",
"nodes": {
"photon.ttk-test.xyz": 1
}
}'
```

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/photon \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
  -d '{
"uri": "/photon/*",
    "plugins": {
      "key-auth": {},
      "cors": {},
     "proxy-rewrite": {
      "regex_uri": ["^/photon/(.*)", "/$1"]
}
    },
"upstream_id": "photon-upstream"
  }'
```

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/consumers/photon-consumer \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
 -d '{
"username": "photon-consumer",
"plugins": {
"key-auth": {
"key": "fcd1c8f035335f136f87ad84b625c8f1"
}
}
}'
```

```
curl -H "apikey: fcd1c8f035335f136f87ad84b625c8f1" "https://api.deploily.cloud/photon/api?q=ain"
```

## ORS

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/ors \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
 -d '{
  "uri": "/ors/v2/*",
"plugins": {
"key-auth": {},
"cors": {}
},
"upstream": {
"nodes": {
"ors.ttk-test.xyz:443": 1
},
"type": "roundrobin",
"scheme": "https",
"pass_host": "rewrite",
"upstream_host": "ors.ttk-test.xyz"
}
}'
```

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/consumers/ors-consumer \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
 -d '{
"username": "ors-consumer",
"plugins": {
"key-auth": {
"key": "bgd1c8f035335f136f87ad84b625c8f1"
}
}
}'
```

```
curl --request POST \
  --url https://api.deploily.cloud/ors/v2/matrix/driving-car \
  --header 'Accept: application/json;charset=UTF-8, */*' \
  --header 'Content-Type: application/json' \
  --header 'apikey: bgd1c8f035335f136f87ad84b625c8f1' \
  --data '{
  "locations": [
    [
      9.70093,
      48.477473
    ],
    [
      9.207916,
      49.153868
    ],
    [
      37.573242,
      55.801281
    ],
    [
      115.663757,
      38.106467
    ]
  ],
  "id": "my_request",
  "sources": [
    "all"
  ],
  "destinations": [
    "all"
  ],
  "metrics": [
    "duration"
  ],
  "resolve_locations": false,
  "units": "m"
}'
```

```
curl --request GET \
  --url https://api.deploily.cloud/ors/v2/status \
  --header 'Accept: */*' \
  --header 'apikey: bgd1c8f035335f136f87ad84b625c8f1'
```

# API WILAYA

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/consumers/api-wilaya-consumer \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
 -d '{
"username": "api-wilaya-consumer",
"plugins": {
"key-auth": {
"key": "rtl1c8f035336f136f87ad84b625c8f1"
}
}
}'

```

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/upstreams/wilaya-upstream \
  -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "roundrobin",
    "scheme": "https",
    "pass_host": "rewrite",
    "upstream_host": "api-wilaya.ttk-test.xyz",
    "nodes": {
      "api-wilaya.ttk-test.xyz": 1
    }
  }'
```

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/wilaya \
  -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
  -H "Content-Type: application/json" \
  -d '{
    "uri": "/wilaya/api/v1/*",
    "plugins": {
      "key-auth": {},
      "cors": {},
      "proxy-rewrite": {
        "regex_uri": ["^/wilaya/api/v1/(.*)", "/api/v1/$1"]
      }
    },
    "upstream_id": "wilaya-upstream"
  }'
```

```
curl --request GET \
  --url 'https://api.deploily.cloud/wilaya/api/v1/getWilaya?lat=35&long=-1.1' \
  --header 'Accept: application/json' \
  --header 'apikey: rtl1c8f035336f136f87ad84b625c8f1'
```

## Nominatim

```

curl -X PUT https://admin-api.deploily.cloud/apisix/admin/upstreams/nominatim-upstream \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
 -d '{
"type": "roundrobin",
"scheme": "https",
"pass_host": "rewrite",
"upstream_host": "nominatim.ttk-test.xyz",
"nodes": {
"nominatim.ttk-test.xyz": 1
}
}'
```

```
curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/nominatim \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -H "Content-Type: application/json" \
  -d '{
"uri": "/nominatim/*",
    "plugins": {
      "key-auth": {},
      "cors": {},
     "proxy-rewrite": {
      "regex_uri": ["^/nominatim/(.*)", "/$1"]
}
    },
"upstream_id": "nominatim-upstream"
  }'
```

** Or with one curl command **

```
 curl -X PUT https://admin-api.deploily.cloud/apisix/admin/routes/nominatim \
  -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
  -H "Content-Type: application/json" \
  -d '{
    "uri": "/nominatim/*",
    "plugins": {
      "key-auth": {},
      "cors": {
        "allow_origins": "*",
        "allow_methods": "GET,POST,PUT,DELETE,OPTIONS",
        "allow_headers": "*",
        "expose_headers": "*",
        "max_age": 3600,
        "allow_credentials": true
      },
      "proxy-rewrite": {
        "regex_uri": ["^/nominatim/(.*)", "/$1"]
      }
    },
    "upstream": {
      "nodes": {
        "nominatim.ttk-test.xyz:443": 1
      },
      "type": "roundrobin",
      "scheme": "https",
      "pass_host": "rewrite",
      "upstream_host": "nominatim.ttk-test.xyz"
    }
  }'
```

```
curl "https://api.deploily.cloud/nominatim/reverse?lat=35.30538822124727&lon=-1.1417971423748299&format=json&accept-language=fr" \
 -H "apikey: rtl1c8f035336f136f87ad84b625c8f1"
```
