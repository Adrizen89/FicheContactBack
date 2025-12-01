# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [1.1.0] - 2025-12-01

### 🎉 Production-Ready Release

#### ✨ Nouvelles fonctionnalités

- **ValidateFicheUsecase** : Nouveau use case pour valider les fiches (Clean Architecture complète)
- **Logging structuré** : JSON logging pour production, format lisible pour dev
- **DTOs API** : Schémas Pydantic dédiés pour séparer domaine et API
- **Healthcheck Docker** : Surveillance automatique des conteneurs

#### 🔧 Améliorations

- **Documentation OpenAPI** : Summary et descriptions sur toutes les routes
- **Typage mypy** : Configuration stricte avec validation automatique
- **Couverture de tests** : pytest-cov configuré et fonctionnel
- **Logs enrichis** : Contexte ajouté sur toutes les opérations (fiche_id, erreurs, etc.)

#### 🐳 DevOps

- **Docker multi-stage** : Build optimisé avec stages séparés
- **docker-compose.yml** : Stack complète (API + PostgreSQL + PgAdmin)
- **GitHub Actions CI/CD** : 4 jobs (tests, lint, build, security)
- **.env.example** : Documentation des variables d'environnement
- **Migrations SQL** : Système de migration avec versioning

#### 🔒 Sécurité

- **CORS strict** : Origines autorisées uniquement
- **Security scan** : Safety check dans CI/CD
- **Secrets protection** : .env.example sans valeurs sensibles
- **Validation stricte** : EmailStr, regex patterns dans DTOs

#### 📝 Documentation

- **REFACTORING.md** : Documentation complète du refactoring
- **IMPROVEMENTS.md** : Guide des améliorations production-ready
- **CHANGELOG.md** : Historique des versions
- **OpenAPI enrichie** : Exemples et descriptions détaillées

#### 🐛 Corrections

- N/A (nouvelle version)

---

## [1.0.0] - 2025-12-01

### 🎯 Refactoring Major Release

#### 🔧 Corrections majeures

- **Repository unifié** : Utilisation cohérente de FicheConverter
- **Gestion des transactions** : Rollback sur toutes les erreurs SQL
- **Méthode update()** : Gestion correcte des works_planned (suppression + recréation)
- **Conversion Enum** : Correction de model.origin_contact.value → model.origin_contact

#### ✨ Améliorations

- **Entité Fiche simplifiée** : Suppression de planned_works et works_details (redondants)
- **Typage complet** : Tous les use cases ont des types de retour explicites
- **Use cases dans l'API** : Plus d'accès direct au repository
- **Messages d'erreur** : Plus clairs et contextuels

#### 📝 Documentation

- README mis à jour avec architecture détaillée
- Tests corrigés et passants (18/18)

---

## [0.1.0] - 2025-05-20

### 🎬 Initial Release

#### ✨ Fonctionnalités initiales

- CRUD complet des fiches clients
- Gestion des travaux planifiés avec validation JSON Schema
- API REST avec FastAPI
- Base de données PostgreSQL
- Tests unitaires avec pytest
- Architecture Clean Architecture (entities, use cases, repositories)

#### 📦 Technologies

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- pytest

---

## Légende

- ✨ Nouvelle fonctionnalité
- 🔧 Amélioration
- 🐛 Correction de bug
- 🔒 Sécurité
- 🐳 DevOps/Infrastructure
- 📝 Documentation
- ⚠️ Breaking change
- 🗑️ Dépréciation

## Format

Ce changelog suit le format [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).
