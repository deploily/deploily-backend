# Checklist Sécurité (CI/CD)

## Variables et secrets
- `SECRET_KEY`, `APISIX_API_KEY`, `KEYCLOAK_CLIENT_SECRET` requis en prod (pas de fallback)
- Scan de secrets (ex.: trufflehog/gitleaks) sur le repo et artefacts

## Auth & JWT
- Algorithme JWT: `RS256` côté Keycloak; vérification côté backend via clé publique/JWKS
- Gestion d’erreurs réseau lors de la récupération de la clé publique (timeouts, retry)

## Sécurité applicative
- CSRF activé
- CORS restreint aux domaines autorisés en prod
- Swagger UI désactivé en prod (activable en dev via `ENABLE_SWAGGER`)

## Dépendances & Qualité
- Audit des dépendances (pip-audit/Safety) avec gating sur `high/critical`
- Linting et tests automatisés (pre-commit, pytest)

## Conteneur & Infra
- Image non-root; `HEALTHCHECK` sur un endpoint de santé
- etcd: authentification obligatoire; pas d’expositions publiques
- APISIX: clé admin locale et sécurisée; pas de `allow_admin: 0.0.0.0/0` hors dev
- Postgres/Redis: éviter identifiants par défaut en prod

## Logs & Observabilité
- Ne pas journaliser d’informations sensibles
- Activer métriques et traces si disponibles

## CI/CD Gating
- Échec si vulnérabilité `high/critical` détectée ou si secrets exposés
- Échec si variables obligatoires manquantes en prod

