# CacaoDetect Backend

API FastAPI pour la détection des maladies du cacaoyer via intelligence artificielle.

## Structure du projet

```
Backend/
├── app/
│   ├── main.py              # Entrée principale FastAPI
│   ├── core/
│   │   ├── config.py        # Configuration et variables d'environnement
│   │   └── security.py      # JWT, bcrypt, authentification
│   ├── models/              # Modèles SQLAlchemy ORM
│   │   ├── utilisateur.py
│   │   ├── analyse.py
│   │   ├── maladie.py
│   │   └── modele_ia.py
│   ├── schemas/             # Schémas Pydantic (validation)
│   │   ├── auth_schema.py
│   │   └── diagnostic_schema.py
│   ├── routers/             # Routes API
│   │   ├── auth.py          # POST /register, /login, /logout, GET /me
│   │   ├── diagnose.py      # POST /diagnose (analyse d'images)
│   │   ├── analyses.py      # GET /analyses, DELETE, EXPORT
│   │   └── admin.py         # Routes administration
│   └── services/            # Couche métier
│       ├── ia_service.py    # Orchestration du modèle IA
│       └── storage_service.py # Gestion des fichiers (local/S3)
├── alembic/                 # Migrations de base de données
├── requirements.txt         # Dépendances Python
├── .env.example            # Template de configuration
└── .env                    # Configuration locale (SECRET)
```

## Prérequis

- Python 3.9+
- PostgreSQL 13+
- pip ou poetry

## Installation

### 1. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données

Créer une base de données PostgreSQL:

```sql
CREATE DATABASE cacaodetect;
CREATE USER cacaouser WITH PASSWORD 'cacaopass';
ALTER ROLE cacaouser SET client_encoding TO 'utf8';
ALTER ROLE cacaouser SET default_transaction_isolation TO 'read committed';
ALTER ROLE cacaouser SET default_transaction_deferrable TO on;
ALTER ROLE cacaouser SET default_transaction_read_uncommitted TO off;
GRANT ALL PRIVILEGES ON DATABASE cacaodetect TO cacaouser;
```

### 4. Configurer les variables d'environnement

Copier `.env.example` en `.env` et adapter les paramètres:

```bash
cp .env.example .env
```

Éditer `.env` avec vos paramètres:
- `DATABASE_URL`: Chaîne de connexion PostgreSQL
- `SECRET_KEY`: Clé secrète pour JWT (générer une clé forte en production)
- `CORS_ORIGINS`: Origines autorisées (inclure `http://localhost:3001`)

### 5. Exécuter les migrations

```bash
alembic upgrade head
```

## Lancement

### Mode développement (avec rechargement automatique)

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Mode production

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

L'API sera disponible sur `http://localhost:8000`

## Documentation API

Une fois le serveur lancé, la documentation interactive est disponible à:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints principaux

### Authentification
- `POST /api/v1/auth/register` - Créer un compte
- `POST /api/v1/auth/login` - Connexion
- `POST /api/v1/auth/logout` - Déconnexion
- `GET /api/v1/auth/me` - Infos utilisateur courant

### Diagnostic
- `POST /api/v1/diagnose` - Analyser une image de feuille

### Analyses
- `GET /api/v1/analyses` - Liste des analyses (paginée)
- `GET /api/v1/analyses/{id}` - Détail d'une analyse
- `DELETE /api/v1/analyses/{id}` - Supprimer une analyse
- `GET /api/v1/analyses/{id}/export` - Exporter en PDF

### Administration
- `GET /api/v1/admin/users` - Liste des utilisateurs
- `PUT /api/v1/admin/users/{id}` - Modifier un utilisateur
- `DELETE /api/v1/admin/users/{id}` - Supprimer un utilisateur
- `GET /api/v1/admin/stats` - Statistiques globales
- `POST /api/v1/admin/modele` - Déployer un nouveau modèle IA

## Architecture

### Authentification JWT

Tous les endpoints (sauf `/register` et `/login`) nécessitent un header:

```
Authorization: Bearer <access_token>
```

### Flux d'enregistrement

1. Utilisateur remplit le formulaire d'inscription
2. Backend hache le mot de passe avec bcrypt
3. Enregistrement en base de données
4. Génération des tokens JWT (access + refresh)
5. Retour des tokens au frontend

### Flux de diagnostic

1. Utilisateur upload une image
2. Validation du fichier (type, taille)
3. Stockage sur disque local ou S3
4. Appel au modèle IA pour analyse
5. Annotation de l'image si détection positive
6. Sauvegarde du résultat en base
7. Retour du diagnostic au frontend

## Développement

### Ajouter une nouvelle route

1. Créer la fonction dans le router approprié
2. Utiliser les dépendances (`get_current_user`, etc.)
3. Utiliser les schémas pour validation/sérialisation
4. Tester avec `curl` ou Postman

### Ajouter un nouveau modèle

1. Créer la classe dans `app/models/`
2. Créer une migration Alembic: `alembic revision --autogenerate -m "Add new table"`
3. Exécuter: `alembic upgrade head`

### Tests

```bash
pytest tests/
```

## Configuration S3 (Optionnel)

Pour utiliser AWS S3 pour le stockage des images:

1. Activer dans `.env`: `USE_S3=True`
2. Ajouter vos credentials AWS
3. Configurer le bucket S3

## Dépannage

### Erreur de connexion à PostgreSQL

```
psycopg2.OperationalError: could not connect to server
```

- Vérifier que PostgreSQL est démarré
- Vérifier `DATABASE_URL` dans `.env`

### Token JWT invalide

```
HTTPException: status_code=401, detail="Token invalide"
```

- Vérifier que le `SECRET_KEY` est le même qu'à la génération
- Vérifier que le token n'a pas expiré

### Fichier trop volumineux

```
HTTPException: status_code=413, detail="Fichier trop volumineux"
```

- Augmenter `MAX_FILE_SIZE_MB` dans `.env`
- Compresser l'image côté frontend

## Contribution

Les contributions sont bienvenues! Veuillez:

1. Créer une branche pour votre feature
2. Faire des commits clairs
3. Pousser et créer une Pull Request

## Licence

MIT
