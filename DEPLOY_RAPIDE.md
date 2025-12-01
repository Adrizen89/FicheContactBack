# 🚀 Déploiement GitHub Actions + VPS Hostinger (Version Simple)

## Étape 1 : Prépare ton VPS (5 min)

Connecte-toi et lance ce script :

```bash
ssh root@VOTRE_IP

# Installation automatique
curl -fsSL https://get.docker.com | sh
useradd -m -s /bin/bash deployer
echo "deployer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
usermod -aG docker deployer
su - deployer
mkdir -p ~/apps/fiche-api
```

## Étape 2 : Configure l'accès SSH avec mot de passe (plus simple que les clés)

Sur le VPS :

```bash
# Définir un mot de passe pour deployer
sudo passwd deployer
# Entre un mot de passe simple (ex: Deploy123!)

# Autoriser l'authentification par mot de passe
sudo nano /etc/ssh/sshd_config
# Trouve la ligne "PasswordAuthentication" et mets "yes"
# Sauvegarde (Ctrl+X, Y, Enter)

sudo systemctl restart sshd
```

## Étape 3 : Configure les secrets GitHub (2 min)

GitHub → Settings → Secrets → New secret

| Secret | Valeur |
|--------|--------|
| `VPS_HOST` | Ton IP (ex: `123.45.67.89`) |
| `VPS_USER` | `deployer` |
| `VPS_PASSWORD` | Le mot de passe que tu viens de créer |
| `DB_PASSWORD` | Un mot de passe pour PostgreSQL (ex: `Postgres123!`) |

## Étape 4 : Push ton code (1 min)

Le workflow `.github/workflows/deploy-simple.yml` est déjà créé et simplifié !

```bash
git add .
git commit -m "feat: Setup simple deployment"
git push origin main
```

## Étape 5 : Regarde la magie opérer ✨

1. Va sur GitHub → Actions
2. Regarde le workflow "Deploy Simple" s'exécuter
3. Après ~2 minutes, ton API est en ligne !

## Étape 6 : Vérifie

```bash
curl http://VOTRE_IP:8000/
# Devrait retourner: {"message":"API en ligne ! ✅"}

# Ouvre dans ton navigateur
http://VOTRE_IP:8000/docs
```

---

## 🎉 C'est tout !

À chaque `git push origin main`, ton app se redéploie automatiquement.

---

## 🔧 Commandes utiles sur le VPS

```bash
# Voir les logs
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs -f fiche-api-prod

# Redémarrer manuellement
docker compose restart api

# Voir l'état
docker ps
```

---

## 📊 Ce qui se passe lors du déploiement

1. GitHub Actions se connecte au VPS via SSH
2. Clone/met à jour ton code
3. Crée automatiquement le `docker-compose.yml`
4. Lance les conteneurs (PostgreSQL + API)
5. Vérifie que l'API répond
6. ✅ Déploiement terminé !

---

## 🆘 Dépannage

**Le workflow échoue ?**
- Vérifie que les 4 secrets GitHub sont bien configurés
- Vérifie que tu peux te connecter : `ssh deployer@VOTRE_IP`

**L'API ne démarre pas ?**
```bash
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs fiche-api-prod
```

**Erreur de base de données ?**
```bash
docker logs fiche-db-prod
```

---

## 🔐 Note de sécurité

Cette version utilise un mot de passe SSH pour simplifier. Pour la production, tu peux passer aux clés SSH plus tard (voir `DEPLOYMENT_HOSTINGER.md`).

---

## 🚀 Prochains déploiements

Maintenant, pour déployer une nouvelle version :

```bash
# Fais tes modifications
git add .
git commit -m "feat: Nouvelle fonctionnalité"
git push origin main

# GitHub Actions déploie automatiquement !
```

C'est aussi simple que ça ! 🎊
