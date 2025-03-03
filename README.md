# Deploily backend 



## Prepare for developement

```bash
cd .devcontainer
cp .env.example .env
pre-commit install
```

Make any relevant modification to suite you local developement environment in the `.env` file, especially the Keycloak `CLIENT_SECRET` and the `APISIX_API_KEY`.

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
flask db revision --rev-id <revision-id>
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
## Run  flask

```bash
cd src
flask run 
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

Realm settings -> Token -> Default Signature Algorithm = HS256

```bash
curl -d 'client_id=[deploily]' -d 'username=[admin]' -d 'password=[admin]' -d 'grant_type=[password]' -d 'scope=email profile roles' -d 'client_secret=[............]' 'https://auth.deploily.cloud/realms/myrealm/protocol/openid-connect/token'
```

To decode the JWT Token use [https://jwt.io/](https://jwt.io/)

## Useful links
