# Rapport d'Audit de Sécurité — deploily-backend

**Date :** 2026-04-07
**Branche auditée :** `audit-security`
**Auditeur :** Claude Sonnet 4.6 (Anthropic)
**Périmètre :** Code source, configuration Docker/APISIX, dépendances, architecture auth

---

## Résumé exécutif

L'audit couvre l'ensemble du dépôt `deploily-backend` : code Python (Flask/Flask-AppBuilder), fichiers de configuration Docker Compose, APISIX, et les dépendances. Six vulnérabilités critiques ont été identifiées, dont deux nécessitent une action immédiate sur l'historique git (rotation de secrets exposés). Le projet présente une base architecturale solide (OAuth2/OIDC via Keycloak, CSRF activé, JWT RS256) mais souffre de lacunes opérationnelles majeures : absence de rate limiting malgré la dépendance installée, CAPTCHA désactivé, et plusieurs secrets hardcodés.

---

## Tableau de bord

| Sévérité | Nombre | Statut recommandé |
|---|---|---|
| CRITIQUE | 7 | Bloquer le déploiement |
| IMPORTANT | 10 | Corriger avant mise en production |
| ATTENTION | 6 | Adresser rapidement post-prod |
| OK | 14 | Points validés |

---

## CRITIQUE — Vulnérabilités bloquantes

### C-1 — Clé Fernet hardcodée avec valeur par défaut publique

**Fichier :** `src/app/core/models/subscription_models.py:31`
**Impact :** Compromission de toutes les API keys chiffrées en base de données

```python
FERNET_KEY = os.getenv("FERNET_KEY", "QkqrpIbcUuQ_5Ho25VEv5oPFN4IVuOYojOMwneVbZNQ=")
```

La clé Fernet utilisée pour chiffrer les `api_key` en BDD possède une valeur par défaut codée en dur dans le code source. Si la variable d'environnement `FERNET_KEY` n'est pas injectée au démarrage, toutes les API keys sont chiffrées avec une clé publiquement connue. Tout attaquant ayant accès à un dump de base de données peut déchiffrer l'ensemble des API keys sans effort.

**Correction :**
- Supprimer le fallback. Utiliser `os.environ["FERNET_KEY"]` (lève une `KeyError` si absent).
- Régénérer une clé Fernet unique par environnement.
- Rechiffrer les données existantes si la clé par défaut a été utilisée en production.

---

### C-2 — Credentials APISIX Admin hardcodés dans le dépôt

**Fichiers :**
- `.devcontainer/apisix_conf/config.yaml:33-38`
- `.devcontainer/dashboard_conf/conf.yaml:56-63`

**Impact :** Prise de contrôle complète du gateway APISIX

```yaml
# apisix_conf/config.yaml
admin_key:
  - name: "admin"
    key: edd1c9f034335f136f87ad84b625c8f1
  - name: "viewer"
    key: 4054f7cf07e344346cd3f287985e76a2
```

```yaml
# dashboard_conf/conf.yaml
authentication:
  secret: secret
users:
  - username: admin
    password: admin
```

Ces credentials sont committés dans l'historique git. Les clés admin APISIX permettent de modifier toutes les routes, upstreams et consumers du gateway. Le dashboard utilise les identifiants par défaut `admin/admin` avec un secret JWT trivial.

**Correction :**
- Exécuter `git filter-repo` pour purger ces fichiers de l'historique.
- Remplacer par des templates utilisant des variables d'environnement.
- Régénérer immédiatement toutes les clés si le dépôt a été partagé ou est public.

---

### C-3 — Interface Admin APISIX exposée sans restriction d'IP

**Fichier :** `.devcontainer/apisix_conf/config.yaml:29-30`
**Impact :** Administration APISIX accessible depuis n'importe quelle IP

```yaml
allow_admin:
  - 0.0.0.0/0   # "We need to restrict ip access rules for security. 0.0.0.0/0 is for test."
```

Le commentaire reconnaît explicitement le problème. L'interface d'administration APISIX (port 9180) est accessible depuis toutes les IPs sans restriction. Combiné avec les clés hardcodées (C-2), cela constitue une surface d'attaque critique.

**Correction :**
- En production : restreindre à `127.0.0.1/32` ou aux IPs du réseau d'administration.
- En développement : utiliser un réseau Docker isolé.

---

### C-4 — IDOR sur l'endpoint d'upload de reçu de paiement

**Fichier :** `src/app/core/controllers/payment_controller.py:114`
**Impact :** Un utilisateur authentifié peut modifier les données d'un autre utilisateur

```python
payment = db.session.query(Payment).filter(Payment.id == payment_id).first()
# Aucune vérification que le paiement appartient à l'utilisateur courant
```

L'endpoint `POST /api/v1/payments/<id>/upload-receipt` ne vérifie pas que le paiement ciblé appartient à l'utilisateur authentifié. En énumérant les IDs (entiers séquentiels), un attaquant peut uploader un faux reçu sur le paiement de n'importe quel autre utilisateur.

**Correction :**
```python
user = get_user()
payment = (
    db.session.query(Payment)
    .filter(Payment.id == payment_id, Payment.created_by == user)
    .first()
)
```

---

### C-5 — Vérification CAPTCHA désactivée pour les paiements

**Fichier :** `src/app/services/subscription_service_base.py:485-488`
**Impact :** Fraude automatisée sur les paiements par carte

```python
# todo Vérification CAPTCHA
# is_valid, error_msg = self.verify_captcha(request_data.captcha_token)
# if not is_valid:
#     return False, error_msg, None
```

La vérification CAPTCHA pour les paiements par carte est intégralement commentée. Conjugué à l'absence de rate limiting (C-6), cela permet des attaques automatisées de fraude par carte (card testing, carding).

**Correction :**
- Décommenter et activer la vérification CAPTCHA.
- Configurer `CAPTCHA_SECRET_KEY` (actuellement `None` via `os.getenv`).

---

### C-6 — Endpoint public sans protection anti-abus

**Fichier :** `src/app/core/controllers/contact_us_controllers.py:65-147`
**Impact :** Spam massif, saturation de la queue mail Celery, déni de service

```python
class PublicContactUSModelApi(BaseApi):
    @expose("/contact-us", methods=["POST"])
    def add_contact_us(self):
        # Pas d'authentification
        # Pas de rate limiting
        # Pas de CAPTCHA
        # Pas de validation d'input
        # Chaque appel enqueue une tâche mail Celery
```

L'endpoint `/api/v1/public/contact-us` est accessible sans aucun mécanisme de protection. Un script trivial peut envoyer des milliers de requêtes, saturant la queue Celery et le serveur mail.

**Correction :**
- Activer Flask-Limiter (déjà installé, jamais instancié).
- Ajouter une validation d'input (longueur max, format email).
- Envisager un CAPTCHA côté frontend.

---

### C-7 — Flask-Limiter installé mais jamais instancié ni utilisé

**Fichier :** `requirements.txt:8`
**Impact :** Aucun rate limiting sur l'ensemble de l'API

```
Flask-Limiter==3.5.1
```

La dépendance est présente mais aucune instance `Limiter` n'existe dans le code. Aucun décorateur `@limiter.limit()` n'a été trouvé sur l'ensemble du codebase. Tous les endpoints — y compris les endpoints sensibles (abonnements, paiements, authentification) — sont illimités.

**Correction :**
```python
# src/app/__init__.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address, default_limits=["200/day", "50/hour"])
```
Puis appliquer des limites strictes sur les endpoints critiques.

---

## IMPORTANT — Risques significatifs

### I-1 — API Tokens stockés en texte clair en base de données

**Fichier :** `src/app/promo_code/models/api_tokens_model.py:12`

```python
token = Column(Text, nullable=False)
```

Les tokens API sont stockés en clair dans la colonne `token`. En cas de dump de base de données (injection SQL, accès non autorisé), tous les tokens sont immédiatement exploitables.

**Correction :** Stocker un hash PBKDF2/bcrypt du token. Afficher le token complet une seule fois lors de sa création.

---

### I-2 — Redis exposé sans authentification sur l'hôte

**Fichier :** `.devcontainer/docker-compose.yml:86-88`

```yaml
redis:
  image: redis:7.2.3-bookworm
  ports:
    - "6379:6379"   # Exposé sur toutes les interfaces, sans mot de passe
```

Redis est exposé sur `0.0.0.0:6379` sans authentification. Il contient les queues Celery (tâches d'envoi d'email, traitements d'abonnements) et le cache applicatif. Un attaquant sur le même réseau peut lire, modifier ou injecter des tâches.

**Correction :** Configurer `requirepass` dans Redis. Utiliser `network_mode` Docker pour isoler le service.

---

### I-3 — PostgreSQL avec credentials par défaut

**Fichier :** `.devcontainer/docker-compose.yml:38`

```yaml
POSTGRES_PASSWORD: postgres
```

Le mot de passe `postgres` est trivial. Si le port 5432 est exposé via le forwarding devcontainer, la base de données est accessible depuis l'hôte sans effort.

---

### I-4 — Alembic expose le mot de passe de BDD dans les logs

**Fichier :** `src/migrations/env.py:29`

```python
return get_engine().url.render_as_string(hide_password=False)
```

`hide_password=False` inclut le mot de passe de la base de données dans l'URL SQLAlchemy rendue en clair dans la sortie de migration et les logs.

**Correction :** `hide_password=True`

---

### I-5 — Upload de fichier sans validation du type MIME

**Fichier :** `src/app/core/controllers/payment_controller.py:118-119`

```python
extension = os.path.splitext(file.filename)[1]   # Contrôlé par le client
filename = f"{uuid.uuid4().hex}{extension}"
```

L'extension est extraite du nom de fichier fourni par le client, non du contenu réel. Il n'y a aucune vérification du type MIME. Le fichier est sauvegardé dans `static/uploads/` servi statiquement. Un attaquant peut uploader un fichier `.html` ou tout autre type non désiré.

**Correction :**
- Utiliser `python-magic` pour valider le type MIME réel.
- Définir une whitelist stricte : `{'image/jpeg', 'image/png', 'application/pdf'}`.
- Ne pas utiliser l'extension fournie par le client pour nommer le fichier sauvegardé.

---

### I-6 — JWT Access Token avec expiration 24h

**Fichier :** `src/config.py:118`

```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
```

Une durée de 24h est excessive pour un access token. En cas de vol de token (XSS, interception), la fenêtre d'exploitation est très large. Aucun mécanisme de refresh token n'est implémenté.

**Recommandation :** Réduire à 15–60 minutes. Implémenter un endpoint de refresh token.

---

### I-7 — Données sensibles exposées via `print()` en production

De nombreux `print()` actifs en production exposent des informations sensibles dans stdout/logs :

| Fichier | Ligne | Données exposées |
|---|---|---|
| `subscription_models.py` | 260 | Erreur de déchiffrement d'API key |
| `subscription_models.py` | 271 | Signal de chiffrement d'API key |
| `subscription_service_base.py` | 512 | Order ID et Form URL SATIM (paiement) |
| `payment_service.py` | 76 | Réponse complète du service de paiement |
| `managed_ressource_controllers.py` | 210, 303 | Résultats bruts de ressources managées |
| `payment_models.py` | 72, 90, 92 | Détails de transactions email/paiement |

**Correction :** Remplacer tous les `print()` par `_logger.debug()` ou `_logger.info()` selon le contexte.

---

### I-8 — CORS URLs hardcodées dans le code source

**Fichier :** `src/app/__init__.py:17-24`

```python
# TODO move urls to .env | localhost should only be available for dev
CORS(app, ..., origins=["http://localhost:3000", "https://console.deploily.cloud"])
```

Les origines CORS sont hardcodées. Le TODO est présent mais non résolu. Cela empêche une configuration flexible par environnement.

**Correction :** Lire les origines depuis `os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")`.

---

### I-9 — IPs internes exposées dans la configuration OpenAPI

**Fichier :** `src/config.py:90-97`

```python
FAB_OPENAPI_SERVERS = [
    {"url": "http://192.168.1.22:5000"},
    {"url": "http://192.168.1.21:5000"},
    {"url": "http://192.168.1.15:5000"},
    {"url": "http://192.168.1.16:5000"},
]
```

Ces adresses IP internes sont visibles via l'interface Swagger et constituent une fuite d'information sur la topologie réseau.

---

### I-10 — Logging de données PII utilisateur

**Fichier :** `src/app/core/controllers/contact_us_controllers.py:117`

```python
_logger.info(f"Received contact us data: {data}")
```

L'objet `data` contient nom, email, téléphone et message de l'utilisateur. Ces données PII sont loguées en clair, en contradiction avec les exigences RGPD.

---

## ATTENTION — Bonnes pratiques manquantes

### A-1 — Dépendances obsolètes avec CVEs potentielles

| Package | Version actuelle | Risque |
|---|---|---|
| `Pillow` | 9.1.1 (2022) | Nombreux CVEs corrigés depuis (buffer overflow, DoS) |
| `Flask` | 2.2.5 | Obsolète, Flask 3.x disponible |
| `Flask-OAuthlib` | 0.9.6 | Non maintenu, remplacé par Authlib (déjà présent) |
| `Flask-SQLAlchemy` | 2.5.1 | Obsolète (3.x disponible) |
| `Flask-AppBuilder` | 4.3.7 | Vérifier les CVEs récents |

**Action :** Exécuter `pip-audit` ou `safety check` pour identifier les CVEs actifs.

---

### A-2 — SQLite comme fallback silencieux en production

**Fichier :** `src/config.py:83-84`

```python
SQLLITE_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", SQLLITE_DATABASE_URI)
```

Si `SQLALCHEMY_DATABASE_URI` n'est pas défini, l'application démarre silencieusement sur SQLite sans aucune alerte. SQLite n'a pas de gestion de concurrence, pas de chiffrement natif, et le fichier `.db` serait dans le container.

**Correction :** Supprimer le fallback ou lever une exception explicite si l'URI pointe vers SQLite en dehors de l'environnement de test.

---

### A-3 — `app.run(debug=True)` dans le fichier d'initialisation

**Fichier :** `src/app/__init__.py:71`

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Le mode debug Werkzeug active un console interactif dans le navigateur permettant l'exécution de code Python arbitraire. Bien que protégé par `if __name__ == "__main__"`, cette ligne dans un fichier d'init est risquée et trompeuse.

---

### A-4 — RECAPTCHA non configuré

**Fichier :** `src/config.py:79-80`

```python
RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""
```

Confirme que la protection CAPTCHA est globalement inopérante sur l'ensemble de l'application.

---

### A-5 — Headers de sécurité HTTP manquants

Aucun middleware de sécurité HTTP (Flask-Talisman ou équivalent) n'est configuré. Les headers suivants sont absents en production :

| Header | Protection |
|---|---|
| `Strict-Transport-Security` | Force HTTPS, prévient le downgrade |
| `X-Content-Type-Options: nosniff` | Prévient le MIME sniffing |
| `X-Frame-Options: DENY` | Prévient le clickjacking |
| `Content-Security-Policy` | Prévient XSS et injection de contenu |
| `Referrer-Policy` | Contrôle les informations de référence |

**Correction :** Ajouter `Flask-Talisman` avec une CSP adaptée.

---

### A-6 — Subscription status non mis à jour automatiquement à l'expiration

**Fichier :** `src/app/schedulers/notify_subscription_expiration.py:33`

```python
# TODO when subscriotion is expired `status` should change to `inactive`
```

Le statut d'abonnement n'est pas automatiquement passé à `inactive` lors de l'expiration. Des abonnements expirés peuvent rester en statut `active` en base, entraînant des incohérences métier.

---

## Points validés

| Point | Détail | Fichier |
|---|---|---|
| `SECRET_KEY` obligatoire | `os.environ["SECRET_KEY"]` — lève une erreur si absent | `config.py:68` |
| `APISIX_API_KEY` obligatoire | `os.environ["APISIX_API_KEY"]` — idem | `config.py:323` |
| JWT algorithme RS256 | Algorithme asymétrique sécurisé, clé publique Keycloak | `config.py:46` |
| Authentification OAuth2/OIDC | Keycloak comme Identity Provider | `config.py:27-42` |
| Filtrage par utilisateur | `base_filters` sur toutes les APIs sensibles | Contrôleurs |
| Swagger désactivé par défaut | `FAB_API_SWAGGER_UI = False` par défaut | `config.py:89` |
| FAB Security API désactivé | `FAB_ADD_SECURITY_API = False` | `config.py:65` |
| CSRF activé | `CSRF_ENABLED = True` | `config.py:88` |
| `secure_filename()` utilisé | Sanitisation du nom de fichier | `payment_controller.py:120` |
| Chiffrement des API keys | Fernet utilisé (voir C-1 pour le fallback) | `subscription_models.py:248` |
| Dockerfile non-root | `USER python` en runtime | `Dockerfile:49` |
| `.env` dans `.gitignore` | Fichier `.env` correctement ignoré | `.gitignore:125` |
| Rôles granulaires | `FAB_ROLES` avec permissions par endpoint | `config.py:144` |
| Auto-registration limité | `AUTH_USER_REGISTRATION_ROLE = "User"` | `config.py:142` |

---

## Plan d'action recommandé

### Phase 1 — Immédiat (avant tout push sur remote)

1. **Purger l'historique git** des credentials APISIX (`git filter-repo --path .devcontainer/apisix_conf/config.yaml --invert-paths`)
2. **Régénérer** toutes les clés APISIX et le secret dashboard
3. **Supprimer le fallback** `FERNET_KEY` hardcodé
4. **Rechiffrer** les données BDD si la clé par défaut a été utilisée

### Phase 2 — Avant déploiement en production

5. Corriger l'**IDOR sur l'upload de reçu** (ajouter filtre `created_by`)
6. **Activer Flask-Limiter** avec des limites sur tous les endpoints publics
7. **Activer le CAPTCHA** sur les paiements par carte
8. **Valider le type MIME** des fichiers uploadés (whitelist stricte)
9. Exécuter **`pip-audit`** et corriger les CVEs critiques (Pillow en priorité)
10. Ajouter **Flask-Talisman** pour les headers HTTP de sécurité

### Phase 3 — Post-déploiement

11. Déplacer les URLs CORS dans les **variables d'environnement**
12. Remplacer tous les **`print()` sensibles** par des appels logger
13. Réduire **JWT expiry** à 30 min + implémenter refresh tokens
14. **Hasher les API tokens** en base de données
15. Corriger `hide_password=False` dans **Alembic**

---

*Rapport généré par audit statique du code source. Un audit de pénétration dynamique est recommandé avant toute mise en production.*
