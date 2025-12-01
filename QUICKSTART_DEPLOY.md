# 🚀 Quick Start - Déploiement VPS Hostinger

Guide rapide pour déployer en 15 minutes chrono ! ⏱️

## ✅ Checklist pré-déploiement

- [ ] Compte Hostinger actif avec VPS
- [ ] Accès SSH au VPS (IP, user, password)
- [ ] Repository GitHub créé
- [ ] Code pushé sur GitHub

---

## 📝 ÉTAPE 1 : Préparer le VPS (5 min)

```bash
# 1. Se connecter au VPS
ssh root@VOTRE_IP

# 2. Tout-en-un : Installation complète
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl enable docker
sudo systemctl start docker

# 3. Créer l'utilisateur de déploiement
sudo useradd -m -s /bin/bash deployer
sudo usermod -aG docker deployer
sudo mkdir -p /home/deployer/.ssh
sudo chmod 700 /home/deployer/.ssh
```

---

## 🔑 ÉTAPE 2 : Configurer SSH (3 min)

### Sur votre machine locale

```bash
# Générer la clé SSH
ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/hostinger_deploy -N ""

# Afficher la clé PUBLIQUE
cat ~/.ssh/hostinger_deploy.pub
# Copier le résultat
```

### Sur le VPS

```bash
# Coller la clé publique
sudo nano /home/deployer/.ssh/authorized_keys
# Coller le contenu et sauvegarder (Ctrl+X, Y, Enter)

# Permissions
sudo chmod 600 /home/deployer/.ssh/authorized_keys
sudo chown -R deployer:deployer /home/deployer/.ssh

# Tester la connexion
exit
ssh -i ~/.ssh/hostinger_deploy deployer@VOTRE_IP
# Si ça marche, vous êtes bon ! ✅
```

---

## 🔐 ÉTAPE 3 : Configurer GitHub Secrets (2 min)

Aller sur GitHub → Settings → Secrets and variables → Actions → New secret

Créer ces 4 secrets :

| Nom | Valeur | Exemple |
|-----|--------|---------|
| `VPS_HOST` | IP du VPS | `123.45.67.89` |
| `VPS_USER` | `deployer` | `deployer` |
| `VPS_PORT` | `22` | `22` |
| `VPS_SSH_KEY` | Clé privée complète | Contenu de `~/.ssh/hostinger_deploy` |
| `DB_PASSWORD` | Mot de passe sécurisé | `VotreMotDePasseSecurise123!` |

**Pour copier la clé privée** :
```bash
cat ~/.ssh/hostinger_deploy
# Copier TOUT le contenu (y compris BEGIN et END)
```

---

## 🚀 ÉTAPE 4 : Premier déploiement (5 min)

### 4.1 Vérifier les fichiers

Assurez-vous que ces fichiers existent dans votre projet :
- ✅ `docker-compose.production.yml`
- ✅ `deploy.sh`
- ✅ `.github/workflows/ci.yml`
- ✅ `Dockerfile`

### 4.2 Push vers GitHub

```bash
git add .
git commit -m "feat: Add production deployment"
git push origin main
```

### 4.3 Suivre le déploiement

1. Aller sur GitHub → Actions
2. Cliquer sur le workflow en cours
3. Suivre les étapes :
   - ✅ Test
   - ✅ Build-and-push
   - ✅ Deploy

### 4.4 Vérifier

```bash
# API
curl http://VOTRE_IP:8000/

# Swagger
open http://VOTRE_IP:8000/docs
```

---

## 🌐 BONUS : Ajouter un domaine (Optionnel)

### Si vous avez un nom de domaine

#### 1. Pointer le domaine vers le VPS

Dans votre registrar (OVH, Gandi, etc.) :
```
Type: A
Nom: api (ou @)
Valeur: VOTRE_IP_VPS
TTL: 3600
```

#### 2. Installer Nginx sur le VPS

```bash
ssh deployer@VOTRE_IP

# Installer Nginx
sudo apt update
sudo apt install -y nginx

# Créer la config
sudo nano /etc/nginx/sites-available/fiche-api
```

Coller :
```nginx
server {
    listen 80;
    server_name api.votredomaine.fr;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Activer :
```bash
sudo ln -s /etc/nginx/sites-available/fiche-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. SSL gratuit avec Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d api.votredomaine.fr
```

**C'est tout ! Votre API est maintenant sur HTTPS** 🔒

---

## 🆘 Dépannage rapide

### Le déploiement échoue

```bash
# Sur le VPS, vérifier les logs
ssh deployer@VOTRE_IP
cd ~/apps/fiche-api
docker logs fiche-api-prod
```

### L'API ne répond pas

```bash
# Redémarrer
cd ~/apps/fiche-api
docker compose -f docker-compose.production.yml restart

# Vérifier les conteneurs
docker ps
```

### Erreur de base de données

```bash
# Voir les logs de la DB
docker logs fiche-db-prod

# Se connecter à la DB
docker exec -it fiche-db-prod psql -U ficheuser fichecontact
```

---

## 📊 Commandes utiles

```bash
# Logs en temps réel
docker logs -f fiche-api-prod

# Redémarrer l'API
cd ~/apps/fiche-api
docker compose -f docker-compose.production.yml restart api

# Tout arrêter
docker compose -f docker-compose.production.yml down

# Sauvegarder la BDD
docker exec fiche-db-prod pg_dump -U ficheuser fichecontact > backup.sql
```

---

## 🎉 C'est fini !

Votre API est maintenant :
- ✅ Déployée automatiquement à chaque push sur `main`
- ✅ Accessible sur http://VOTRE_IP:8000
- ✅ Documentée sur http://VOTRE_IP:8000/docs
- ✅ Avec base de données PostgreSQL
- ✅ Avec sauvegardes automatiques

**Prochains déploiements** : Juste `git push origin main` ! 🚀

---

## 📚 Aller plus loin

- 📖 Guide complet : `docs/DEPLOYMENT_HOSTINGER.md`
- 🐛 Problèmes : Créer une issue GitHub
- 💡 Améliorations : Voir `IMPROVEMENTS.md`

Bon déploiement ! 🎊
