# CacaoDetect Backend - Documentation API

## Vue d'ensemble

L'API CacaoDetect fournit les endpoints pour:
- Authentification (login, register, refresh token)
- Diagnostic des maladies (upload et analyse d'images)
- Gestion de l'historique des analyses
- Administration du système

**Base URL**: `http://localhost:8000/api/v1`
**Version**: 1.0.0

## Authentification

Tous les endpoints (sauf `/auth/register` et `/auth/login`) nécessitent un token JWT.

### Format du header

```
Authorization: Bearer <access_token>
```

### Cycle de vie du token

1. `access_token`: Valide 60 minutes (configurable)
2. `refresh_token`: Valide 7 jours

Quand `access_token` expire, utiliser `refresh_token` pour en obtenir un nouveau.

## Endpoints

### Authentication

#### `POST /auth/register`

Enregistrer un nouvel utilisateur.

**Request Body:**
```json
{
  "email": "user@example.com",
  "nom": "Dupont",
  "prenom": "Jean",
  "password": "SecurePassword123",
  "role": "agriculteur"  // "agriculteur" | "agronome" | "chercheur"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id_utilisateur": 1,
    "email": "user@example.com",
    "nom": "Dupont",
    "prenom": "Jean",
    "role": "agriculteur",
    "date_inscription": "2026-07-01T10:00:00"
  }
}
```

**Erreurs:**
- `400`: Email déjà utilisé ou données invalides
- `422`: Validation échouée

#### `POST /auth/login`

Se connecter avec email et mot de passe.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": { ... }
}
```

**Erreurs:**
- `401`: Email ou mot de passe invalide
- `422`: Validation échouée

#### `POST /auth/logout`

Se déconnecter (invalide le token côté client).

**Header requis:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "message": "Déconnexion réussie"
}
```

#### `GET /auth/me`

Récupérer les informations de l'utilisateur courant.

**Header requis:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "id_utilisateur": 1,
  "email": "user@example.com",
  "nom": "Dupont",
  "prenom": "Jean",
  "role": "agriculteur",
  "date_inscription": "2026-07-01T10:00:00"
}
```

**Erreurs:**
- `401`: Token invalide ou expiré

### Diagnosis

#### `POST /diagnose`

Analyser une image de feuille de cacaoyer.

**Headers requis:**
- `Authorization: Bearer <access_token>`
- `Content-Type: multipart/form-data`

**Form Data:**
- `file`: Image (JPEG/PNG, max 10 Mo)
- `notes`: (optionnel) Notes de l'utilisateur

**Response (200):**
```json
{
  "id_analyse": 42,
  "date_heure": "2026-07-01T10:30:00",
  "statut": "termine",
  "duree_traitement_s": 2.5,
  "flag_avertissement": false,
  "diagnostic": {
    "id_diagnostic": 100,
    "maladie": {
      "id_maladie": 1,
      "nom_maladie": "Pourriture brune",
      "agent_causal": "Phytophthora spp.",
      "organes_touches": "Cabosses, tiges",
      "description": "Infection fongique affectant les cabosses",
      "recommandations": [
        {
          "id_recommandation": 1,
          "traitement": "Fongicide",
          "produit": "Copper sulphate",
          "dosage": "2 kg/ha",
          "frequence": "Tous les 14 jours",
          "source": "FAO"
        }
      ]
    },
    "niveau_gravite": "modere",
    "score_confiance": 0.87,
    "bbox": [100, 50, 300, 250],
    "chemin_image_annotee": "./uploads/annotated_20260701_103000.jpg",
    "flag_avertissement": false
  }
}
```

**Erreurs:**
- `400`: Fichier invalide ou trop volumineux
- `401`: Non authentifié
- `413`: Fichier trop volumineux
- `422`: Validation échouée
- `500`: Erreur du modèle IA

### History & Analyses

#### `GET /analyses`

Lister les analyses de l'utilisateur.

**Headers requis:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `page`: int (default: 1, min: 1)
- `limit`: int (default: 10, max: 100)
- `maladie`: string (optionnel, filter par nom de maladie)
- `gravite`: string (optionnel, "faible" | "modere" | "eleve")
- `date_debut`: string (optionnel, format: "YYYY-MM-DD")
- `date_fin`: string (optionnel, format: "YYYY-MM-DD")

**Response (200):**
```json
{
  "analyses": [
    {
      "id_analyse": 42,
      "date_heure": "2026-07-01T10:30:00",
      "statut": "termine",
      "maladie_nom": "Pourriture brune",
      "niveau_gravite": "modere",
      "score_confiance": 0.87,
      "image_annotee_url": "./uploads/annotated_20260701_103000.jpg"
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 10
}
```

**Erreurs:**
- `401`: Non authentifié
- `422`: Paramètres invalides

#### `GET /analyses/{id_analyse}`

Récupérer le détail d'une analyse.

**Headers requis:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "id_analyse": 42,
  "date_heure": "2026-07-01T10:30:00",
  "statut": "termine",
  "duree_traitement_s": 2.5,
  "flag_avertissement": false,
  "diagnostic": { ... }
}
```

**Erreurs:**
- `401`: Non authentifié
- `404`: Analyse non trouvée
- `403`: Accès refusé (pas le propriétaire)

#### `DELETE /analyses/{id_analyse}`

Supprimer une analyse.

**Headers requis:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "message": "Analyse supprimée"
}
```

**Erreurs:**
- `401`: Non authentifié
- `404`: Analyse non trouvée
- `403`: Accès refusé

#### `GET /analyses/{id_analyse}/export`

Exporter une analyse en PDF.

**Headers requis:** `Authorization: Bearer <access_token>`

**Response (200):**
File (application/pdf)

**Erreurs:**
- `401`: Non authentifié
- `404`: Analyse non trouvée

### Administration

#### `GET /admin/users`

Lister tous les utilisateurs (admin seulement).

**Headers requis:** 
- `Authorization: Bearer <access_token>` (must be admin)

**Query Parameters:**
- `page`: int (default: 1)
- `limit`: int (default: 10)

**Response (200):**
```json
{
  "users": [
    {
      "id_utilisateur": 1,
      "email": "user@example.com",
      "nom": "Dupont",
      "prenom": "Jean",
      "role": "agriculteur",
      "statut": true
    }
  ],
  "total": 5,
  "page": 1,
  "limit": 10
}
```

**Erreurs:**
- `401`: Non authentifié
- `403`: Accès refusé (non admin)

#### `PUT /admin/users/{id_utilisateur}`

Modifier un utilisateur (admin seulement).

**Headers requis:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "nom": "Dupont",
  "prenom": "Jean",
  "role": "agronome",
  "statut": true
}
```

**Response (200):**
```json
{
  "message": "Utilisateur modifié"
}
```

#### `DELETE /admin/users/{id_utilisateur}`

Supprimer un utilisateur (admin seulement).

**Headers requis:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "message": "Utilisateur supprimé"
}
```

#### `GET /admin/stats`

Récupérer les statistiques globales (admin seulement).

**Headers requis:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "total_utilisateurs": 42,
  "total_analyses": 1250,
  "analyses_aujourd_hui": 35,
  "taux_detection": 0.78,
  "maladie_plus_frequente": "Pourriture brune"
}
```

#### `POST /admin/modele`

Déployer un nouveau modèle IA (admin seulement).

**Headers requis:**
- `Authorization: Bearer <access_token>`
- `Content-Type: multipart/form-data`

**Form Data:**
- `file`: Modèle IA (fichier .h5)
- `version`: string (ex: "1.1.0")

**Response (201):**
```json
{
  "id_modele": 2,
  "version": "1.1.0",
  "date_deploiement": "2026-07-01T10:30:00",
  "actif": true
}
```

## Codes d'erreur HTTP

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Ressource créée |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Accès refusé |
| 404 | Ressource non trouvée |
| 413 | Fichier trop volumineux |
| 422 | Validation échouée |
| 500 | Erreur serveur |

## Exemples curl

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123"
  }'
```

### Analyser une image
```bash
curl -X POST http://localhost:8000/api/v1/diagnose \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@image.jpg" \
  -F "notes=Feuille avec taches brunes"
```

### Lister les analyses
```bash
curl -X GET "http://localhost:8000/api/v1/analyses?page=1&limit=10&gravite=modere" \
  -H "Authorization: Bearer <access_token>"
```

## Rate Limiting

Non implémenté actuellement. À ajouter en production.

## CORS

Les origines suivantes sont autorisées en développement:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`

À configurer en production dans `.env`.

## Versions

- **v1.0.0**: Version initiale
