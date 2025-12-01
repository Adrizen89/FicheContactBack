# ✅ Checklist de Déploiement GitHub Actions + VPS

## 🎯 Configuration VPS (5 minutes)

### Option A : Script automatique (recommandé)

```bash
# Depuis ta machine locale
ssh root@VOTRE_IP 'bash -s' < setup-vps.sh

# Puis définir le mot de passe
ssh root@VOTRE_IP
passwd deployer
# Entre ton mot de passe (note-le bien !)
```

### Option B : Commandes manuelles

```bash
ssh root@VOTRE_IP

# 1. Installer Docker
curl -fsSL https://get.docker.com | sh

# 2. Créer l'utilisateur
useradd -m -s /bin/bash deployer
usermod -aG docker deployer

# 3. Définir le mot de passe
passwd deployer

# 4. Activer l'authentification par mot de passe
nano /etc/ssh/sshd_config
# Trouver "PasswordAuthentication" et mettre "yes"
# Sauvegarder : Ctrl+X, Y, Enter

systemctl restart sshd
```

---

## 🔐 Configuration GitHub Secrets (2 minutes)

Va sur : `https://github.com/TON_USERNAME/tdd_fiche/settings/secrets/actions`

Clique sur **New repository secret** et ajoute ces 4 secrets :

- [ ] `VPS_HOST` → Ton IP VPS (ex: `123.45.67.89`)
- [ ] `VPS_USER` → `deployer`
- [ ] `VPS_PASSWORD` → Le mot de passe que tu as défini
- [ ] `DB_PASSWORD` → Un mot de passe pour PostgreSQL (ex: `PostgreSQL2024!`)

---

## 🚀 Premier Déploiement (1 minute)

```bash
git add .
git commit -m "feat: Setup GitHub Actions deployment"
git push origin main
```

Ensuite :

1. Va sur GitHub → **Actions**
2. Regarde le workflow **Deploy Simple** s'exécuter
3. Après ~2 minutes : ✅ Déployé !

---

## ✅ Vérification

```bash
# Test rapide
curl http://VOTRE_IP:8000/

# Devrait retourner :
# {"message":"API en ligne ! ✅"}
```

Ouvre dans ton navigateur :
- API : `http://VOTRE_IP:8000/`
- Documentation : `http://VOTRE_IP:8000/docs`

---

## 🎉 C'est tout !

Maintenant à chaque `git push origin main`, ton API se redéploie automatiquement.

---

## 🔧 Commandes utiles

```bash
# Voir les logs de l'API
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs -f fiche-api-prod

# Redémarrer manuellement
docker compose restart api

# Voir les conteneurs en cours
docker ps

# Arrêter tout
docker compose down

# Redémarrer tout
docker compose up -d
```

---

## 🆘 En cas de problème

### Le workflow GitHub Actions échoue

1. Vérifie que les 4 secrets sont bien configurés
2. Vérifie que tu peux te connecter : `ssh deployer@VOTRE_IP`
3. Regarde les logs dans GitHub Actions

### L'API ne démarre pas

```bash
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs fiche-api-prod
```

### Erreur de base de données

```bash
docker logs fiche-db-prod
```

### Réinitialiser complètement

```bash
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker compose down -v  # ⚠️ Supprime aussi les données !
rm -rf data/
git pull origin main
docker compose up -d
```

---

## 📚 Documentation complète

- 📖 [DEPLOY_RAPIDE.md](DEPLOY_RAPIDE.md) - Guide détaillé
- 🏗️ [DEPLOYMENT_HOSTINGER.md](docs/DEPLOYMENT_HOSTINGER.md) - Version production avec clés SSH
- 🎯 [SIMPLE_DEPLOY.md](SIMPLE_DEPLOY.md) - Alternatives (Render.com, etc.)

---

## 🔄 Workflow de développement

```bash
# 1. Développe en local
git checkout -b feature/ma-nouvelle-feature

# 2. Teste
pytest tests/

# 3. Commit et push
git add .
git commit -m "feat: Ma nouvelle fonctionnalité"
git push origin feature/ma-nouvelle-feature

# 4. Créer une Pull Request sur GitHub

# 5. Merge dans main
# → Le déploiement automatique se déclenche !
```

---

## 🎊 Prochaines étapes (optionnel)

- [ ] Configurer un nom de domaine
- [ ] Ajouter SSL/HTTPS avec Let's Encrypt
- [ ] Installer Nginx en reverse proxy
- [ ] Configurer des backups automatiques
- [ ] Passer aux clés SSH (voir DEPLOYMENT_HOSTINGER.md)
