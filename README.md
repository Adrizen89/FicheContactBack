# Fiche API - Backend FastAPI

API REST pour la gestion de fiches de contact et de travaux, utilisable avec une application frontend Vue.js.

## ✨ Fonctionnalités principales
- Création de fiches
- Lecture et modification de fiches
- Suppression de fiches
- Ajout de travaux à une fiche selon un schéma dynamique JSON
- Validation de fiche (passage à "terminée")

## 🔍 Structure du projet (extrait)
```
infrastructure/
  api/main.py             <- Point d'entrée FastAPI
  database/fiche_model.py <- Modèle SQLAlchemy
  repositories/           <- Repositories (SQLiteFicheRepository)
contact_fiche/
  entities/               <- Entités Pydantic : Fiche, WorksPlanned...
  enums.py                <- Enums : Status, OriginContact
  contact_fiche_usecases.py <- Usecase CompletionFicheUsecase
config/
  work_schemas.json       <- Schémas JSON dynamiques pour les travaux
```

## 🚀 Lancer le serveur
```bash
uvicorn infrastructure.api.main:app --reload
```

Accéder à Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔗 Routes principales

### ✅ Fiches

#### Créer une fiche
```http
POST /fiche
```
Body (JSON):
```json
{
  "id": "fiche-id",
  "firstname": "Jean",
  "lastname": "Dupont",
  "email": "jean@mail.com",
  "telephone": "0601020304",
  "address": "10 rue X",
  "code_postal": "75000",
  "ville": "Paris",
  "origin_contact": "telephone",
  "status": "en_cours",
  "commentary": "1er contact"
}
```

#### Lire une fiche par ID
```http
GET /fiche/{fiche_id}
```

#### Mettre à jour une fiche
```http
PATCH /fiche/{fiche_id}
```
Body: identique à la création, avec les champs à modifier.

#### Supprimer une fiche
```http
DELETE /fiche/{fiche_id}
```

#### Obtenir les fiches en cours
```http
GET /fiche/en-cours
```
Retourne les fiches avec `status = en_cours`.

#### Valider une fiche
```http
PUT /fiche/{fiche_id}/valider
```
Change le `status` en `terminee`

---

### 📂 Travaux sur fiche

#### Récupérer un schéma JSON selon le type de travaux
```http
GET /schema/{work}
```
Ex : `fenetre`, `porte`, `volet`...

#### Ajouter des travaux à une fiche
```http
PUT /fiche/{fiche_id}/travaux
```
Body :
```json
{
  "works_planned": [
    {
      "work": "fenetre",
      "details": {
        "largeur": 120,
        "hauteur": 150,
        "couleur": "blanc"
      }
    }
  ]
}
```

> Cette route appelle le usecase `CompletionFicheUsecase` qui valide les données par rapport au schéma.

## 🚫 Erreurs courantes
- `404 Not Found` : fiche non trouvée
- `400 Bad Request` : validation des travaux échouée
- `422 Unprocessable Entity` : données JSON mal formées

## ⚒️ Prochaines évolutions possibles
- Authentification JWT
- Filtres par statut, origine du contact, date...
- Historique des actions / audit trail

---

Made with ❤️ par Adrien

