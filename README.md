
## Run  flask

```bash
cd src
flask run 
```
## Migration steps 
First time
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask db revision --rev-id a3bf43e917a8
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

## Run Test
```bash
cd src/tests  
```
Test All
```bash
pytest --disable-warnings -s
```
## Get Keycloack login token 

Realm settings -> Token -> Default Signature Algorithm = HS256

```bash
curl -d 'client_id=deploily' -d 'username=admin' -d 'password=admin' -d 'grant_type=password' -d 'scope=email profile roles'  -d 'client_secret=ZqSIfjStWP3Ztzq5cmcaP6lLGg9kUyMs' 'https://auth.deploily.cloud/realms/myrealm/protocol/openid-connect/token'
```


To decode the JWT Token use [https://jwt.io/](https://jwt.io/)