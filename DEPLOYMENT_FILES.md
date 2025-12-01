# 📁 Fichiers de Déploiement - Vue d'ensemble

Ce document explique tous les fichiers de déploiement créés pour le projet.

---

## 🎯 Pour démarrer rapidement

**Commence par ici** → [START_HERE.md](START_HERE.md)

---

## 📚 Fichiers de documentation

### Guides pour débutants

| Fichier | Description | Temps | Public |
|---------|-------------|-------|--------|
| **[START_HERE.md](START_HERE.md)** | **Point d'entrée principal** - Les 3 étapes essentielles | 8 min | Tous |
| [CHECKLIST.md](CHECKLIST.md) | Checklist complète avec cases à cocher | 10 min | Débutants |
| [DEPLOY_RAPIDE.md](DEPLOY_RAPIDE.md) | Guide détaillé étape par étape avec mot de passe SSH | 10 min | Débutants |

### Guides avancés

| Fichier | Description | Temps | Public |
|---------|-------------|-------|--------|
| [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md) | Déploiement avec clés SSH sécurisées | 15 min | Intermédiaire |
| [docs/DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md) | Guide complet pour production avec SSL, Nginx, etc. | 30 min | Avancé |
| [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) | Résumé technique de l'architecture CI/CD | Lecture | DevOps |

### Alternatives

| Fichier | Description | Public |
|---------|-------------|--------|
| [SIMPLE_DEPLOY.md](SIMPLE_DEPLOY.md) | Options alternatives (Render.com, Docker Compose local, etc.) | Tous |

---

## 🛠️ Scripts utilitaires

### Scripts d'installation

| Script | Description | Usage |
|--------|-------------|-------|
| `setup-vps.sh` | Installation automatique du VPS (Docker + utilisateur) | `ssh root@IP 'bash -s' < setup-vps.sh` |
| `check-deployment.sh` | Vérification de l'état du déploiement | `./check-deployment.sh VOTRE_IP` |

### Workflows GitHub Actions

| Fichier | Description | Déclenchement |
|---------|-------------|---------------|
| `.github/workflows/deploy-simple.yml` | **Workflow simplifié** (mot de passe SSH) | Push sur `main` |
| `.github/workflows/ci.yml` | Workflow complet (5 jobs : test, lint, build, security, deploy) | Push sur `main` |

**Note** : Un seul workflow s'exécute à la fois. Le fichier `deploy-simple.yml` est recommandé pour démarrer.

---

## 🐳 Fichiers Docker

### Fichiers de configuration

| Fichier | Description | Environnement |
|---------|-------------|---------------|
| `Dockerfile` | Image Docker multi-stage optimisée | Production |
| `docker-compose.yml` | Stack locale (API + PostgreSQL + PgAdmin) | Développement |
| `docker-compose.production.yml` | Stack production (API + PostgreSQL) | Production (VPS) |
| `.dockerignore` | Fichiers à exclure du build Docker | Tous |

### Scripts de déploiement

| Script | Description | Usage |
|--------|-------------|-------|
| `deploy.sh` | Script de déploiement manuel avec backup BDD | Sur le VPS uniquement |

---

## ⚙️ Fichiers de configuration

### Configuration du projet

| Fichier | Description |
|---------|-------------|
| `.env.example` | Template des variables d'environnement |
| `pyproject.toml` | Configuration mypy et pytest |
| `requirements.txt` | Dépendances Python |

### Migration base de données

| Fichier | Description |
|---------|-------------|
| `migrations/001_remove_obsolete_columns.sql` | Migration SQL pour nettoyer les colonnes obsolètes |

---

## 📋 Fichiers métadonnées

| Fichier | Description |
|---------|-------------|
| `IMPROVEMENTS.md` | Liste des améliorations apportées au projet |
| `CHANGELOG.md` | Journal des modifications |
| `REFACTORING.md` | Documentation du refactoring effectué |
| `DEPLOYMENT_FILES.md` | Ce fichier - Vue d'ensemble des fichiers de déploiement |

---

## 🎯 Quel fichier utiliser ?

### Tu veux déployer rapidement ?
→ [START_HERE.md](START_HERE.md)

### Tu veux une checklist à suivre ?
→ [CHECKLIST.md](CHECKLIST.md)

### Tu veux comprendre l'architecture ?
→ [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

### Tu veux un déploiement production sécurisé ?
→ [docs/DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md)

### Tu ne veux pas gérer de VPS ?
→ [SIMPLE_DEPLOY.md](SIMPLE_DEPLOY.md) (Option Render.com)

---

## 🔄 Workflows disponibles

### Option 1 : Workflow simplifié (recommandé pour débuter)

**Fichier** : `.github/workflows/deploy-simple.yml`

**Avantages** :
- ✅ Simple : utilise un mot de passe SSH
- ✅ Rapide : déploie en ~2 minutes
- ✅ Automatique : à chaque push sur `main`

**Secrets requis** :
- `VPS_HOST`
- `VPS_USER`
- `VPS_PASSWORD`
- `DB_PASSWORD`

**Documentation** : [DEPLOY_RAPIDE.md](DEPLOY_RAPIDE.md)

---

### Option 2 : Workflow complet (production)

**Fichier** : `.github/workflows/ci.yml`

**Avantages** :
- ✅ Tests automatiques + couverture
- ✅ Linting (Black, isort, flake8)
- ✅ Build Docker optimisé
- ✅ Security scan
- ✅ Backups automatiques
- ✅ Clés SSH sécurisées

**Secrets requis** :
- `VPS_HOST`
- `VPS_USER`
- `VPS_SSH_KEY` (clé privée)
- `VPS_PORT`
- `DB_PASSWORD`

**Documentation** : [QUICKSTART_DEPLOY.md](QUICKSTART_DEPLOY.md), [docs/DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md)

---

## 🔒 Secrets GitHub nécessaires

### Version simple (deploy-simple.yml)

```
VPS_HOST       → IP du VPS (ex: 123.45.67.89)
VPS_USER       → deployer
VPS_PASSWORD   → Mot de passe SSH de l'utilisateur deployer
DB_PASSWORD    → Mot de passe PostgreSQL
```

### Version complète (ci.yml)

```
VPS_HOST       → IP du VPS
VPS_USER       → deployer
VPS_SSH_KEY    → Clé privée SSH (contenu de ~/.ssh/id_ed25519)
VPS_PORT       → 22
DB_PASSWORD    → Mot de passe PostgreSQL
```

---

## 📦 Arborescence des fichiers

```
tdd_fiche/
├── 📖 Documentation déploiement
│   ├── START_HERE.md ⭐ (commence ici !)
│   ├── CHECKLIST.md
│   ├── DEPLOY_RAPIDE.md
│   ├── QUICKSTART_DEPLOY.md
│   ├── SIMPLE_DEPLOY.md
│   ├── DEPLOYMENT_SUMMARY.md
│   ├── DEPLOYMENT_FILES.md (ce fichier)
│   └── docs/
│       └── DEPLOYMENT_HOSTINGER.md
│
├── 🛠️ Scripts
│   ├── setup-vps.sh
│   ├── check-deployment.sh
│   └── deploy.sh
│
├── ⚙️ Configuration
│   ├── .env.example
│   ├── pyproject.toml
│   └── requirements.txt
│
├── 🐳 Docker
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.production.yml
│   └── .dockerignore
│
├── 🚀 GitHub Actions
│   └── .github/workflows/
│       ├── deploy-simple.yml ⭐ (recommandé)
│       ├── ci.yml
│       └── README.md
│
└── 🗄️ Migrations
    └── migrations/
        └── 001_remove_obsolete_columns.sql
```

---

## 🎊 Résumé

**Pour déployer maintenant** :
1. Lis [START_HERE.md](START_HERE.md)
2. Exécute `setup-vps.sh` sur ton VPS
3. Configure les 4 secrets GitHub
4. Push sur `main`
5. Regarde la magie opérer ! ✨

**Pour comprendre l'architecture** :
- Lis [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)

**Pour la production** :
- Suis [docs/DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md)

---

Tous les fichiers sont prêts ! Tu n'as plus qu'à choisir ton parcours. 🚀
