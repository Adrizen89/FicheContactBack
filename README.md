# Fiche API - Backend FastAPI

API REST pour la gestion de fiches de contact client dans le secteur de la menuiserie (fenêtres, portes, volets, stores, etc.).

## 📋 À propos du projet

Ce backend FastAPI permet de gérer des fiches clients avec leurs informations de contact, rendez-vous et travaux planifiés. Il utilise une architecture Clean Architecture avec séparation des couches (entities, use cases, repositories, infrastructure).

## ✨ Fonctionnalités principales

- **Gestion CRUD des fiches** : Création, lecture, modification et suppression de fiches client
- **Gestion des travaux** : Ajout de travaux planifiés avec validation JSON Schema dynamique
- **Statuts de fiche** : Suivi du statut (Default, In Progress, Completed)
- **Schémas dynamiques** : Configuration JSON pour différents types de travaux (fenêtre, porte, volet, store, etc.)
- **Base de données PostgreSQL** : Stockage persistant avec SQLAlchemy
- **Tests unitaires** : Suite de tests avec pytest

## 🏗️ Architecture du projet

### Structure des dossiers
```
tdd_fiche/
├── contact_fiche/                    # Domain layer (Clean Architecture)
│   ├── entities/
│   │   ├── fiche_entity.py          # Entité Fiche (Pydantic)
│   │   └── works_planned_entity.py  # Entité WorksPlanned
│   ├── enums.py                     # Enums : Status, OriginContact, Material
│   ├── contact_fiche_usecases.py    # Use cases métier
│   ├── fiche_repository_protocol.py # Interface du repository
│   └── in_memory_fiche_repository.py # Repository en mémoire (tests)
│
├── infrastructure/                   # Infrastructure layer
│   ├── api/
│   │   └── main.py                  # Point d'entrée FastAPI, routes
│   ├── database/
│   │   ├── connexion.py             # Connexion PostgreSQL via SQLAlchemy
│   │   ├── fiche_model.py           # Modèle SQLAlchemy (FicheModel, WorkPlannedModel)
│   │   └── fiche_converter.py       # Conversion Entity ↔ Model
│   └── repositories/
│       └── sqlite_fiche_repository.py # Repository SQLite/PostgreSQL
│
├── config/                           # Configuration
│   ├── work_schemas.json            # Schémas JSON pour validation des travaux
│   ├── config_works.json            # Configuration alternative
│   └── works_schemas_config.py      # Service de chargement des schémas
│
├── tests/                           # Tests unitaires
│   └── test_contact_fiche.py        # Suite de tests pytest
│
├── main.py                          # Script de test/démo
├── requirements.txt                 # Dépendances Python
└── README.md
```

### Principes architecturaux

- **Clean Architecture** : Séparation claire entre domain, use cases et infrastructure
- **Dependency Injection** : Utilisation de FastAPI Depends pour l'injection de dépendances
- **Repository Pattern** : Abstraction de la persistance via des protocoles
- **Validation par schémas** : Validation dynamique des données via JSON Schema

## 🚀 Installation et démarrage

### Prérequis
- Python 3.12+
- PostgreSQL (ou SQLite pour le développement)
- Docker et Docker Compose (optionnel)

### Installation locale

1. Cloner le projet et installer les dépendances :
```bash
git clone https://github.com/votre-username/tdd_fiche.git
cd tdd_fiche
pip install -r requirements.txt
```

2. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

3. Lancer avec Docker (recommandé) :
```bash
docker-compose up -d
```

Ou sans Docker :
```bash
uvicorn infrastructure.api.main:app --reload
```

4. Accéder à la documentation :
- API : [http://localhost:8000](http://localhost:8000)
- Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc : [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Tests

```bash
# Tests unitaires
pytest tests/ -v

# Avec couverture
pytest --cov=contact_fiche --cov=infrastructure --cov-report=html

# Type checking
mypy contact_fiche/ infrastructure/
```

### Déploiement

Le projet est configuré pour un déploiement automatique sur VPS Hostinger via GitHub Actions.

**🎯 [COMMENCE ICI ➡️ START_HERE.md](START_HERE.md)** - Guide en 3 étapes (8 minutes)

📖 **Autres guides de déploiement** :
- ✅ [Checklist complète](CHECKLIST.md) - Toutes les étapes détaillées
- ⚡ [Déploiement Rapide](DEPLOY_RAPIDE.md) - Version simplifiée avec mot de passe
- 🚀 [Quick Start](QUICKSTART_DEPLOY.md) - Version avec clés SSH (15 min)
- 📚 [Guide complet production](docs/DEPLOYMENT_HOSTINGER.md) - Version avancée
- 📋 [Résumé technique](DEPLOYMENT_SUMMARY.md) - Architecture CI/CD
- 🎯 [Déploiement sans VPS](SIMPLE_DEPLOY.md) - Alternatives (Render.com, etc.)

## 🔗 API - Routes principales

### Routes de base

#### Status de l'API
```http
GET /
```
Retourne `{"message": "API en ligne ! ✅"}`

---

### Gestion des fiches

#### Créer une fiche
```http
POST /fiche
```
**Body** (exemple) :
```json
{
  "id": "abc123",
  "firstname": "Jean",
  "lastname": "Dupont",
  "date_rdv": "2025-01-15",
  "heure_rdv": "14:00",
  "email": "jean.dupont@mail.com",
  "telephone": "0601020304",
  "address": "10 rue de la Paix",
  "code_postal": "75000",
  "city": "Paris",
  "type_logement": "Maison",
  "statut_habitation": "Propriétaire",
  "origin_contact": "Salon",
  "planned_works": ["fenetre", "porte"],
  "commentary": "Premier contact suite au salon"
}
```

#### Lire une fiche par ID
```http
GET /fiche/{fiche_id}
```

#### Lire toutes les fiches
```http
GET /fiches
```

#### Lire les fiches en cours
```http
GET /fiches/en-cours
```
Retourne uniquement les fiches avec `status = "In Progress"`.

#### Mettre à jour une fiche
```http
PATCH /fiche/{fiche_id}
```
Body : objet Fiche avec les champs à modifier.

#### Valider une fiche (passage à "terminée")
```http
PUT /fiche/{fiche_id}/valider
```
Change le `status` en `"Completed"`. Body : objet Fiche complet.

#### Supprimer une fiche
```http
DELETE /fiche/{fiche_id}
```

#### Récupérer les villes distinctes
```http
GET /fiches/villes
```
Retourne la liste des villes uniques des fiches existantes.

---

### Gestion des travaux

#### Récupérer le schéma JSON d'un type de travaux
```http
GET /schema/{work}
```
Exemples de `work` : `fenetre`, `porte_entree`, `volet_roulant`, `volet_battant`, `store_exterieur`, `store_interieur`, `portail`, `pergola`, `porte_de_garage`, `cloture`.

**Réponse** : Schéma JSON Schema pour valider les détails du travail.

#### Ajouter des travaux validés à une fiche
```http
PUT /fiche/{fiche_id}/travaux
```
**Body** :
```json
{
  "works_planned": [
    {
      "work": "fenetre",
      "details": {
        "material_color": {
          "materiau": "PVC",
          "color": "BLANC"
        },
        "choice_piece": "Salon",
        "type_pose": "Renovation",
        "type_window": "Fenetre 2 vantaux",
        "hauteur": 150,
        "largeur": 120,
        "allege": "Non",
        "hab_int": "Oui",
        "hab_ext": "Non",
        "grille_ventilation": "Oui",
        "commentary": "https://image.com/photo.jpg"
      }
    }
  ]
}
```

> Cette route valide les données via le `CompletionFicheUsecase` qui vérifie la conformité avec le schéma JSON correspondant au type de travail. En cas de succès, le statut passe automatiquement à `"Completed"`.

## 🔧 Modèle de données

### Entité Fiche (`contact_fiche/entities/fiche_entity.py`)

| Champ | Type | Description |
|-------|------|-------------|
| `id` | `str` | Identifiant unique |
| `firstname` | `str` | Prénom du client |
| `lastname` | `str` | Nom de famille |
| `date_rdv` | `str` | Date du rendez-vous |
| `heure_rdv` | `str` | Heure du rendez-vous |
| `telephone` | `str` | Numéro de téléphone |
| `email` | `str` | Adresse email |
| `address` | `str` | Adresse complète |
| `code_postal` | `str` | Code postal |
| `city` | `str` | Ville |
| `type_logement` | `str` | Type de logement (Maison, Appartement, etc.) |
| `statut_habitation` | `str` | Statut (Propriétaire, Locataire, etc.) |
| `origin_contact` | `OriginContact` | Origine du contact (Salon, Ancien client, Réseaux sociaux, Affichage) |
| `planned_works` | `List[str]` | Liste des types de travaux prévus |
| `works_details` | `List[Dict]` | Détails supplémentaires sur les travaux |
| `works_planned` | `List[WorksPlanned]` | Travaux planifiés avec validation |
| `commentary` | `str` | Commentaire libre |
| `status` | `Status` | Statut de la fiche (Default, In Progress, Completed) |

### Enums

**OriginContact** (`contact_fiche/enums.py:4`)
- `SALON` : "Salon"
- `CLIENT` : "Ancien client"
- `RS` : "Réseaux sociaux"
- `AFFICHAGE` : "Affichage"

**Material** (`contact_fiche/enums.py:10`)
- `PVC`
- `BOIS`
- `ALU`

**Status** (`contact_fiche/enums.py:15`)
- `DEFAULT` : Fiche créée mais pas encore traitée
- `IN_PROGRESS` : Fiche en cours de traitement
- `COMPLETED` : Fiche validée/terminée

## 🧪 Use Cases

Le projet implémente plusieurs use cases métier (`contact_fiche/contact_fiche_usecases.py`) :

### CreateFicheUsecase (`contact_fiche/contact_fiche_usecases.py:21`)
Crée une nouvelle fiche et la passe automatiquement au statut `IN_PROGRESS`.

### UpdateFicheUsecase (`contact_fiche/contact_fiche_usecases.py:54`)
Met à jour partiellement une fiche existante (tous les champs sont optionnels).

### DeleteFicheUsecase (`contact_fiche/contact_fiche_usecases.py:103`)
Supprime une fiche par son ID.

### CompletionFicheUsecase (`contact_fiche/contact_fiche_usecases.py:110`)
Ajoute des travaux validés à une fiche :
1. Vérifie que la fiche existe
2. Valide chaque travail avec son schéma JSON correspondant
3. Assigne les travaux à la fiche
4. Passe le statut à `COMPLETED`

## 📐 Schémas de travaux

Les schémas de validation sont définis dans `config/work_schemas.json`. Chaque type de travaux possède son propre schéma JSON Schema.

### Types de travaux supportés
- **fenetre** : Fenêtre avec matériau, couleur, dimensions, type de pose, etc.
- **porte_entree** : Porte d'entrée avec tirant, allège, dimensions
- **volet_roulant** / **volet_battant** : Volets avec pose et dimensions
- **store_exterieur** / **store_interieur** : Stores avec manœuvre et couleur
- **portail** : Portails
- **pergola** : Pergolas
- **porte_de_garage** : Portes de garage
- **cloture** : Clôtures

### Exemple de validation
Lorsqu'un travail de type `"fenetre"` est ajouté, le système :
1. Récupère le schéma depuis `WorkSchemaConfigService` (`config/works_schemas_config.py:15`)
2. Valide les `details` avec `jsonschema.validate()`
3. Rejette la requête si les données ne respectent pas le schéma

## 🔒 Sécurité et CORS

Le serveur FastAPI implémente :
- **CORS** : Autorise toutes les origines (`allow_origins=['*']`) - à restreindre en production
- **Middleware de restriction d'origine** (`infrastructure/api/main.py:130`) : Limite l'accès aux origines autorisées
  - `https://pro-fiche.vercel.app` (production)
  - `http://localhost:5173` (développement)

## 🚫 Gestion des erreurs

| Code HTTP | Description |
|-----------|-------------|
| `200 OK` | Succès |
| `400 Bad Request` | Validation des travaux échouée ou données invalides |
| `403 Forbidden` | Origine non autorisée |
| `404 Not Found` | Fiche non trouvée |
| `422 Unprocessable Entity` | Données JSON mal formées (Pydantic) |

## 🧩 Stack technique

- **FastAPI** : Framework web asynchrone
- **Pydantic** : Validation de données et sérialisation
- **SQLAlchemy** : ORM pour PostgreSQL
- **jsonschema** : Validation JSON Schema
- **pytest** : Framework de tests
- **psycopg2-binary** : Driver PostgreSQL
- **python-dotenv** : Gestion des variables d'environnement
- **uvicorn** : Serveur ASGI

## 📝 Notes de développement

### Base de données
Le projet utilise PostgreSQL en production (via `DATABASE_URL`). Les modèles sont définis dans `infrastructure/database/fiche_model.py` :
- **FicheModel** : Table principale des fiches
- **WorkPlannedModel** : Table des travaux planifiés (relation 1-N avec FicheModel)

### Tests
Les tests utilisent un `InMemoryFicheRepository` pour ne pas dépendre de la base de données. Suite complète dans `tests/test_contact_fiche.py`.

### Frontend
Ce backend est conçu pour être utilisé avec une application Vue.js frontend déployée sur Vercel (`https://pro-fiche.vercel.app`).

## ⚒️ Évolutions possibles

- Authentification JWT pour sécuriser les endpoints
- Filtres avancés (par date, statut, ville, origine)
- Pagination des résultats
- Historique des modifications (audit trail)
- Upload d'images/photos pour les travaux
- Génération de devis PDF
- Système de notifications (email, SMS)

---

Made with ❤️ par Adrien

