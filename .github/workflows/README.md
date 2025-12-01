# Workflows GitHub Actions

Ce projet contient deux workflows de déploiement :

## 🚀 deploy-simple.yml (RECOMMANDÉ pour débuter)

**Utilise celui-ci si tu veux déployer rapidement !**

- ✅ Simple : utilise un mot de passe SSH
- ✅ Rapide : déploie en ~2 minutes
- ✅ Automatique : à chaque push sur `main`
- ✅ Moins de configuration requise

**Secrets nécessaires** :
- `VPS_HOST` : IP du VPS
- `VPS_USER` : `deployer`
- `VPS_PASSWORD` : mot de passe SSH
- `DB_PASSWORD` : mot de passe PostgreSQL

**Documentation** : Voir `DEPLOY_RAPIDE.md`

---

## 🏗️ ci.yml (Version complète - Production)

**Utilise celui-ci pour un environnement de production avancé**

- ✅ 5 jobs : Test, Lint, Build, Security, Deploy
- ✅ Build Docker avec GitHub Container Registry
- ✅ Clés SSH sécurisées
- ✅ Tests automatiques et couverture de code
- ✅ Sauvegardes automatiques de la BDD

**Secrets nécessaires** :
- `VPS_HOST` : IP du VPS
- `VPS_USER` : `deployer`
- `VPS_SSH_KEY` : clé privée SSH (pas de mot de passe)
- `VPS_PORT` : `22`
- `DB_PASSWORD` : mot de passe PostgreSQL

**Documentation** : Voir `DEPLOYMENT_HOSTINGER.md`, `QUICKSTART_DEPLOY.md`, `DEPLOYMENT_SUMMARY.md`

---

## ⚙️ Comment choisir ?

| Critère | deploy-simple.yml | ci.yml |
|---------|-------------------|--------|
| Configuration | 5 min | 15-20 min |
| Sécurité | Moyenne (mot de passe) | Haute (clés SSH) |
| Tests automatiques | ❌ | ✅ |
| Build Docker | ❌ | ✅ |
| Linting | ❌ | ✅ |
| Backups BDD | ❌ | ✅ |
| Idéal pour | Développement, prototypes | Production |

---

## 🎯 Recommandation

1. **Pour commencer** : Utilise `deploy-simple.yml`
2. **Quand tu es prêt pour la production** : Passe à `ci.yml`

---

## 🔄 Activer un seul workflow à la fois

Pour désactiver un workflow sans le supprimer, renomme-le :

```bash
# Désactiver deploy-simple.yml
mv .github/workflows/deploy-simple.yml .github/workflows/deploy-simple.yml.disabled

# Réactiver
mv .github/workflows/deploy-simple.yml.disabled .github/workflows/deploy-simple.yml
```

Ou commente la section `on:` dans le fichier.
