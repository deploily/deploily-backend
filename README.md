# Deploily backend 



## Prepare for developement

```bash
cd .devcontainer
cp .env.example .env
pre-commit install
```

Make any relevant modification to suite you local developement environment in the `.env` file, especially the Keycloak `KEYCLOAK_CLIENT_SECRET` and the `APISIX_API_KEY`.

## Database Migration steps 

First time
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

In case you don't have the same migrations history
```bash
flask db migrate -m "<message>"
# copy the revision id in the error message
flask db revision --rev-id 16f6241d9d69
flask db upgrade
```

After updates 
```bash
flask db migrate
flask db upgrade
```
## Create admin user

```bash
flask fab create-admin
```
## Run flask

```bash
cd src
flask run 
```

## add value to ENUM

Connect to the database
```bash
docker exec -it  deploily-backend-db psql -U postgres -d deploily
```
Add new type 
```sql
SELECT 
    column_name, 
    udt_name AS enum_type_name
FROM 
    information_schema.columns 
WHERE 
    table_name = 'managed_ressource' 
    AND data_type = 'USER-DEFINED';

ALTER TYPE <data_type_name> ADD VALUE IF NOT EXISTS '<value>';
```

## Run Test
```bash
cd src/tests  
```

Test All
```bash
pytest --disable-warnings -s
```

## Run pre-commit

```bash
pre-commit run --all-files
```

## Get Keycloack login token 

Realm settings -> Token -> Default Signature Algorithm = RS256

## Get Keycloack login token using localhost

Realm settings -> Token -> Default Signature Algorithm = RS256

```bash
curl -d 'client_id=deploily' \
     -d 'username=admin' \
     -d 'password=admin' \
     -d 'grant_type=password' \
     -d 'scope=email profile roles' \
     -d "client_secret=${KEYCLOAK_CLIENT_SECRET}" \
     'http://localhost:8080/realms/myrealm/protocol/openid-connect/token'
```

## Local Keycloak (dev)
- Démarrer Keycloak local (par ex. via docker) et créer un realm `myrealm`.
- Créer un client confidentiel `deploily` avec scope `openid email profile roles`.
- Conserver l’algorithme par défaut RS256; récupérer la clé publique via l’endpoint realm (`/realms/<realm>` ou JWKS).
- Renseigner dans `.env`:
  - `KEYKCLOAK_URL="http://localhost:8080"`
  - `KEYCLOAK_REALM_NAME="myrealm"`
  - `KEYCLOAK_CLIENT_SECRET="<secret local>"`

## Local APISIX (dev)
- Démarrer APISIX local (et etcd) via `.devcontainer/docker-compose.yml`.
- Définir une clé admin locale et sécurisée; ne pas utiliser les clés de démo.
- Renseigner dans `.env`:
  - `APISIX_ADMIN_URL="http://localhost:9180"`
  - `APISIX_API_KEY="<clé admin locale>"`

To decode the JWT Token use [https://jwt.io/](https://jwt.io/)

## Useful links

## Development Guides
- Guide local Keycloak/APISIX: [dev-local-deployment.md](file:///c:/PythonProjects/transformatek/deploily-backend/docs/dev-local-deployment.md)
- Checklist sécurité CI/CD: [security-checklist.md](file:///c:/PythonProjects/transformatek/deploily-backend/docs/security-checklist.md)
