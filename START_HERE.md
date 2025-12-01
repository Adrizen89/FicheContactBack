# 🎯 COMMENCE ICI !

## Version Simple : GitHub Actions + VPS Hostinger

Tu veux déployer ton API avec GitHub Actions sur ton VPS ? Suis ces 3 étapes.

---

## 📋 Ce dont tu as besoin

- [ ] Un VPS Hostinger actif
- [ ] L'IP de ton VPS
- [ ] Accès root au VPS (via SSH)
- [ ] Ton projet pushé sur GitHub

---

## 🚀 Les 3 étapes

### Étape 1️⃣ : Configure ton VPS (5 min)

**Option automatique** (recommandé) :

```bash
# Depuis ta machine locale
ssh root@VOTRE_IP 'bash -s' < setup-vps.sh

# Puis définir le mot de passe pour deployer
ssh root@VOTRE_IP
passwd deployer
# Entre un mot de passe et note-le !
exit
```

**Option manuelle** : Voir [DEPLOY_RAPIDE.md](DEPLOY_RAPIDE.md#étape-1--prépare-ton-vps-5-min)

---

### Étape 2️⃣ : Configure GitHub (2 min)

1. Va sur : `https://github.com/TON_USERNAME/tdd_fiche/settings/secrets/actions`
2. Clique **New repository secret**
3. Ajoute ces 4 secrets :

```
VPS_HOST       → Ton IP (ex: 123.45.67.89)
VPS_USER       → deployer
VPS_PASSWORD   → Le mot de passe que tu as créé à l'étape 1
DB_PASSWORD    → Un mot de passe pour PostgreSQL (ex: Postgres123!)
```

---

### Étape 3️⃣ : Déploie ! (1 min)

```bash
git add .
git commit -m "feat: Setup deployment"
git push origin main
```

Puis :
1. Va sur GitHub → **Actions**
2. Regarde le workflow s'exécuter (~2 min)
3. ✅ C'est en ligne !

---

## ✅ Vérifie que ça marche

**Option 1 : Avec le script**

```bash
./check-deployment.sh VOTRE_IP
```

**Option 2 : Manuellement**

```bash
curl http://VOTRE_IP:8000/
# Devrait afficher : {"message":"API en ligne ! ✅"}
```

Ouvre dans ton navigateur :
- 🌐 API : `http://VOTRE_IP:8000/`
- 📚 Documentation : `http://VOTRE_IP:8000/docs`

---

## 🎉 Terminé !

Maintenant, **à chaque fois que tu fais `git push origin main`**, ton API se redéploie automatiquement !

---

## 📚 Documentation

- 📖 [CHECKLIST.md](CHECKLIST.md) - Checklist complète étape par étape
- ⚡ [DEPLOY_RAPIDE.md](DEPLOY_RAPIDE.md) - Guide détaillé
- 🔧 [Commandes utiles](#commandes-utiles)

---

## 🔧 Commandes utiles

```bash
# Voir les logs de l'API
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs -f fiche-api-prod

# Redémarrer l'API
docker compose restart api

# Voir l'état des conteneurs
docker ps

# Arrêter tout
docker compose down

# Relancer tout
docker compose up -d
```

---

## 🆘 Problèmes ?

### ❌ Le workflow GitHub Actions échoue

1. Vérifie que les 4 secrets sont bien configurés dans GitHub
2. Vérifie que tu peux te connecter : `ssh deployer@VOTRE_IP`
3. Regarde les logs dans GitHub Actions

### ❌ L'API ne répond pas

```bash
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs fiche-api-prod
```

### ❌ Erreur de base de données

```bash
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs fiche-db-prod
```

### 🔄 Tout réinitialiser

```bash
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker compose down -v
rm -rf data/
git pull origin main
docker compose up -d
```

---

## 🎊 Prochaines étapes (optionnel)

Une fois que tout fonctionne, tu peux :

- [ ] Ajouter un nom de domaine (ex: `api.monsite.fr`)
- [ ] Activer HTTPS avec Let's Encrypt (SSL gratuit)
- [ ] Passer aux clés SSH pour plus de sécurité
- [ ] Configurer des backups automatiques

Voir [DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md) pour ces étapes avancées.

---

## 🔄 Workflow de développement

```bash
# 1. Crée une branche
git checkout -b feature/ma-feature

# 2. Code et teste
pytest tests/

# 3. Commit
git add .
git commit -m "feat: Ma nouvelle fonctionnalité"

# 4. Push
git push origin feature/ma-feature

# 5. Crée une Pull Request sur GitHub

# 6. Merge dans main
# → Déploiement automatique ! 🚀
```

---

**Tout est prêt ! Commence par l'étape 1 👆**
