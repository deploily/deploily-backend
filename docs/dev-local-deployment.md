# Guide de déploiement local (Keycloak & APISIX)

## Prérequis
- Docker et Docker Compose installés
- Fichier `.devcontainer/.env` configuré à partir de `.env.example`
- Variables d’environnement définies:
  - `SECRET_KEY`
  - `KEYCLOAK_CLIENT_SECRET`
  - `APISIX_API_KEY`

## Keycloak local
- Démarrer Keycloak local (exemple):
  - `docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:24.0.5 start-dev`
- Créer le realm `myrealm`
- Créer un client confidentiel `deploily` avec scopes `openid email profile roles`
- Laisser l’algorithme par défaut `RS256` (recommandé)
- Récupérer le `client_secret` et le définir dans `.env`:
  - `KEYKCLOAK_URL="http://localhost:8080"`
  - `KEYCLOAK_REALM_NAME="myrealm"`
  - `KEYCLOAK_CLIENT_SECRET="<secret local>"`

## APISIX local
- Utiliser `.devcontainer/docker-compose.yml` pour démarrer APISIX, APISIX Dashboard, etcd
- Définir une clé admin locale et la fournir via `.env`:
  - `APISIX_ADMIN_URL="http://localhost:9180"`
  - `APISIX_API_KEY="<clé admin locale>"`
- Ne pas exposer `allow_admin: 0.0.0.0/0` hors dev et ne pas utiliser les clés de démo en prod

## Application backend
- Définir `SECRET_KEY` avec une valeur forte et unique
- Optionnel: `ENABLE_SWAGGER="True"` pour activer Swagger en dev
- Lancer l’application:
  - `cd src && flask run` ou via scripts Docker (`/start`)

## Vérifications
- Authentification via Keycloak fonctionne et les tokens sont signés en `RS256`
- APISIX admin accessible à `http://localhost:9180` avec la clé admin locale
- CSRF activé et CORS restreint pour les environnements non-dev

