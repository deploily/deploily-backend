
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
