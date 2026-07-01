# Installation et Démarrage - CacaoDetect Backend

## Prérequis

### Système
- Python 3.9 ou plus récent
- PostgreSQL 13 ou plus récent (optionnel pour développement local)
- Git

### Vérification

```bash
python --version          # Doit être 3.9+
psql --version           # Optional: PostgreSQL
```

## Étapes d'installation

### 1️⃣ Cloner / Naviguer vers le projet

```bash
cd Backend
```

### 2️⃣ Créer un environnement virtuel Python

#### Sur Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Sur Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Sur Windows (CMD):
```bash
python -m venv venv
venv\Scripts\activate.bat
```

### 3️⃣ Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Durée estimée**: 2-5 minutes

### 4️⃣ Configurer la base de données (optionnel)

Pour le développement initial sans PostgreSQL:

Vous pouvez utiliser SQLite ou ignorer la base de données.
Pour utiliser PostgreSQL complet:

#### Créer la base de données:

```bash
# Connectez-vous à PostgreSQL
psql -U postgres

# Créer la DB et l'utilisateur
CREATE DATABASE cacaodetect;
CREATE USER cacaouser WITH PASSWORD 'cacaopass';
GRANT ALL PRIVILEGES ON DATABASE cacaodetect TO cacaouser;
\q
```

### 5️⃣ Configurer les variables d'environnement

```bash
# Copier le fichier template
cp .env.example .env

# Éditer le fichier .env avec vos paramètres
# Pour développement, il suffit souvent de laisser les valeurs par défaut
```

**Vérifier le fichier .env:**
```bash
# Vérifier que ces paramètres sont configurés:
- DATABASE_URL (optionnel, par défaut SQLite en développement)
- SECRET_KEY (générer une clé aléatoire)
- CORS_ORIGINS (inclure http://localhost:3001 pour le frontend)
```

### 6️⃣ Initialiser la base de données

```bash
# Exécuter les migrations
alembic upgrade head

# Charger les données de test (optionnel)
python alembic/seed_data.py
```

## Démarrage

### Mode développement (avec rechargement automatique)

```bash
# Méthode 1: Utiliser le script startup.py
python startup.py

# Méthode 2: Utiliser uvicorn directement
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Output attendu:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Application startup complete
```

### Mode production

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Vérification

Une fois démarré, vérifier que tout fonctionne:

### ✓ Endpoints santé

```bash
# Health check
curl http://localhost:8000/health

# Réponse attendue:
# {"status":"healthy","app":"CacaoDetect","version":"1.0.0"}
```

### ✓ Documentation API

Visiter dans le navigateur:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### ✓ Test login

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "nom": "Test",
    "prenom": "User",
    "password": "TestPassword123",
    "role": "agriculteur"
  }'
```

## Connexion au Frontend

Dans le projet Frontend, assurez-vous que l'API URL pointe vers le backend:

**Frontend/.env:**
```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

Redémarrer le frontend:
```bash
cd Frontend
npm start
```

Maintenant vous pouvez créer un compte depuis l'interface web.

## Dépannage

### ❌ Erreur: ModuleNotFoundError: No module named 'fastapi'

**Solution:**
```bash
# Vérifier que venv est activé
# Puis réinstaller
pip install -r requirements.txt
```

### ❌ Erreur: Address already in use (:8000)

**Solution:**
```bash
# Utiliser un port différent
python -m uvicorn app.main:app --reload --port 8001
```

### ❌ Erreur: could not connect to server (PostgreSQL)

**Solutions:**
1. Vérifier que PostgreSQL est installé et en cours d'exécution
2. Vérifier DATABASE_URL dans .env
3. Pour développement, ignorer la BD pour l'instant

### ❌ JWT Secret Key error

**Solution:**
```bash
# Générer une clé sécurisée
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copier la sortie dans .env comme SECRET_KEY
```

### ❌ Problème CORS

**Solution:**
Vérifier que CORS_ORIGINS dans .env inclut l'origine du frontend:
```
CORS_ORIGINS=["http://localhost:3001"]
```

## Prochaines étapes

1. ✅ Backend API prêt
2. ✅ Frontend connecté (voir Frontend/README.md)
3. ⏳ Implémenter les routes avec vraie logique
4. ⏳ Connecter le modèle IA réel
5. ⏳ Configurer S3 pour les uploads
6. ⏳ Ajouter des tests unitaires

## Documentation complète

- [README.md](./README.md) - Présentation générale
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - Endpoints détaillés
- [Architecture Docs](./docs/ARCHITECTURE.md) - Vue d'ensemble technique

## Support

Pour des questions ou problèmes:
1. Vérifier la documentation
2. Consulter les logs (sortie console)
3. Vérifier les fichiers de configuration (.env)
