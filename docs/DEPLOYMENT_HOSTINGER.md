# 🚀 Guide de déploiement CI/CD sur VPS Hostinger

Ce guide complet vous permettra de mettre en place un pipeline CI/CD automatisé depuis GitHub vers votre VPS Hostinger.

## 📋 Prérequis

### Sur votre VPS Hostinger
- Ubuntu 20.04+ ou Debian 11+
- Accès root ou sudo
- Minimum 2GB RAM, 2 vCPUs
- Au moins 20GB d'espace disque

### Sur GitHub
- Repository du projet
- Accès aux Settings → Secrets

### Domaine (optionnel mais recommandé)
- Nom de domaine pointant vers votre VPS
- Exemple : `api.fb-menuiseries.fr`

---

## 🎯 Architecture cible

```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│   GitHub    │─────▶│  VPS        │─────▶│  PostgreSQL  │
│   Actions   │ SSH  │  Docker     │      │  Database    │
└─────────────┘      │  + Nginx    │      └──────────────┘
                     └─────────────┘
                           │
                           │ Port 80/443
                           ▼
                     ┌──────────────┐
                     │   Internet   │
                     └──────────────┘
```

---

## 📦 ÉTAPE 1 : Préparer le VPS Hostinger

### 1.1 Se connecter au VPS

```bash
ssh root@votre-ip-vps
```

### 1.2 Mettre à jour le système

```bash
apt update && apt upgrade -y
```

### 1.3 Installer Docker et Docker Compose

```bash
# Installer les dépendances
apt install -y apt-transport-https ca-certificates curl software-properties-common

# Ajouter la clé GPG Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Ajouter le repository Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Vérifier l'installation
docker --version
docker compose version
```

### 1.4 Créer un utilisateur de déploiement

```bash
# Créer l'utilisateur
useradd -m -s /bin/bash deployer

# Ajouter au groupe Docker
usermod -aG docker deployer

# Créer le dossier SSH
mkdir -p /home/deployer/.ssh
chmod 700 /home/deployer/.ssh

# Changer le propriétaire
chown -R deployer:deployer /home/deployer
```

### 1.5 Configurer SSH pour GitHub Actions

```bash
# Générer une clé SSH (sur votre machine locale)
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions_deploy

# Sur le VPS, ajouter la clé publique
nano /home/deployer/.ssh/authorized_keys
# Coller le contenu de github_actions_deploy.pub

# Définir les permissions
chmod 600 /home/deployer/.ssh/authorized_keys
chown deployer:deployer /home/deployer/.ssh/authorized_keys
```

### 1.6 Créer la structure de dossiers

```bash
# En tant que deployer
su - deployer

# Créer les dossiers
mkdir -p ~/apps/fiche-api
mkdir -p ~/apps/fiche-api/data/postgres

# Donner les permissions
chmod 755 ~/apps/fiche-api
```

---

## 🔐 ÉTAPE 2 : Configurer les secrets GitHub

Aller dans **Settings → Secrets and variables → Actions** de votre repository GitHub.

### Secrets à créer

| Nom du secret | Valeur | Description |
|---------------|--------|-------------|
| `VPS_HOST` | `123.45.67.89` | IP de votre VPS Hostinger |
| `VPS_USER` | `deployer` | Utilisateur de déploiement |
| `VPS_SSH_KEY` | `[contenu de github_actions_deploy]` | Clé privée SSH |
| `VPS_PORT` | `22` | Port SSH (généralement 22) |
| `DB_PASSWORD` | `votre_mot_de_passe_sécurisé` | Mot de passe PostgreSQL |
| `DOMAIN_NAME` | `api.fb-menuiseries.fr` | Votre domaine (optionnel) |

---

## 📝 ÉTAPE 3 : Créer les fichiers de déploiement

### 3.1 docker-compose.production.yml

Créez ce fichier dans votre projet :

```yaml
version: '3.8'

services:
  api:
    image: ghcr.io/${GITHUB_REPOSITORY}:${IMAGE_TAG}
    container_name: fiche-api-prod
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://ficheuser:${DB_PASSWORD}@db:5432/fichecontact
      - ENVIRONMENT=production
      - DEBUG=False
      - LOG_LEVEL=INFO
    depends_on:
      db:
        condition: service_healthy
    networks:
      - fiche-network
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    container_name: fiche-db-prod
    restart: unless-stopped
    environment:
      POSTGRES_DB: fichecontact
      POSTGRES_USER: ficheuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
      - ./migrations:/docker-entrypoint-initdb.d
    networks:
      - fiche-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ficheuser -d fichecontact"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  fiche-network:
    driver: bridge
```

### 3.2 deploy.sh

Script de déploiement à créer dans votre projet :

```bash
#!/bin/bash

# Couleurs pour les logs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Déploiement de Fiche API${NC}"

# Variables d'environnement
export IMAGE_TAG=${1:-latest}
export DB_PASSWORD=${DB_PASSWORD}
export GITHUB_REPOSITORY=${GITHUB_REPOSITORY}

# Vérifier que DB_PASSWORD est défini
if [ -z "$DB_PASSWORD" ]; then
    echo -e "${RED}❌ DB_PASSWORD non défini${NC}"
    exit 1
fi

# Se déplacer dans le dossier de l'application
cd ~/apps/fiche-api || exit 1

echo -e "${GREEN}✅ Arrêt des conteneurs existants...${NC}"
docker compose -f docker-compose.production.yml down

echo -e "${GREEN}✅ Pull de la nouvelle image...${NC}"
docker compose -f docker-compose.production.yml pull

echo -e "${GREEN}✅ Démarrage des nouveaux conteneurs...${NC}"
docker compose -f docker-compose.production.yml up -d

echo -e "${GREEN}✅ Nettoyage des images inutilisées...${NC}"
docker image prune -f

echo -e "${GREEN}✅ Affichage des conteneurs en cours...${NC}"
docker ps

echo -e "${BLUE}🎉 Déploiement terminé !${NC}"
```

Rendez le script exécutable :
```bash
chmod +x deploy.sh
```

---

## 🔄 ÉTAPE 4 : Modifier le workflow GitHub Actions

Remplacez `.github/workflows/ci.yml` par :

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Job 1: Tests (inchangé)
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_DB: fichecontact_test
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      env:
        DATABASE_URL: postgresql://test_user:test_password@localhost:5432/fichecontact_test
        ENVIRONMENT: test
        DEBUG: False
      run: |
        pytest tests/ -v --cov=contact_fiche --cov=infrastructure --cov-report=xml

    - name: Type checking with mypy
      run: |
        mypy contact_fiche/ infrastructure/ --ignore-missing-imports

  # Job 2: Build et Push de l'image Docker
  build-and-push:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Log in to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # Job 3: Déploiement sur VPS
  deploy:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Deploy to VPS
      uses: appleboy/ssh-action@v1.0.0
      with:
        host: ${{ secrets.VPS_HOST }}
        username: ${{ secrets.VPS_USER }}
        key: ${{ secrets.VPS_SSH_KEY }}
        port: ${{ secrets.VPS_PORT }}
        script: |
          # Se placer dans le dossier de l'app
          cd ~/apps/fiche-api

          # Télécharger les fichiers de config
          curl -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
               -H 'Accept: application/vnd.github.v3.raw' \
               -o docker-compose.production.yml \
               -L https://api.github.com/repos/${{ github.repository }}/contents/docker-compose.production.yml

          curl -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
               -H 'Accept: application/vnd.github.v3.raw' \
               -o deploy.sh \
               -L https://api.github.com/repos/${{ github.repository }}/contents/deploy.sh

          chmod +x deploy.sh

          # Définir les variables d'environnement
          export DB_PASSWORD="${{ secrets.DB_PASSWORD }}"
          export GITHUB_REPOSITORY="${{ github.repository }}"
          export IMAGE_TAG="latest"

          # Exécuter le déploiement
          ./deploy.sh latest

    - name: Health Check
      run: |
        sleep 30
        curl -f http://${{ secrets.VPS_HOST }}:8000/ || exit 1
```

---

## 🌐 ÉTAPE 5 : Configurer Nginx (Optionnel mais recommandé)

### 5.1 Installer Nginx

```bash
# Sur le VPS
apt install -y nginx
```

### 5.2 Créer la configuration Nginx

```bash
nano /etc/nginx/sites-available/fiche-api
```

Contenu :

```nginx
server {
    listen 80;
    server_name api.fb-menuiseries.fr;  # Remplacer par votre domaine

    # Logs
    access_log /var/log/nginx/fiche-api-access.log;
    error_log /var/log/nginx/fiche-api-error.log;

    # Limites
    client_max_body_size 10M;

    # Proxy vers l'API Docker
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        access_log off;
        proxy_pass http://localhost:8000/;
    }
}
```

### 5.3 Activer la configuration

```bash
# Créer le lien symbolique
ln -s /etc/nginx/sites-available/fiche-api /etc/nginx/sites-enabled/

# Tester la configuration
nginx -t

# Recharger Nginx
systemctl reload nginx
```

---

## 🔒 ÉTAPE 6 : SSL avec Let's Encrypt (Recommandé)

### 6.1 Installer Certbot

```bash
apt install -y certbot python3-certbot-nginx
```

### 6.2 Obtenir un certificat SSL

```bash
certbot --nginx -d api.fb-menuiseries.fr
```

Suivez les instructions interactives.

### 6.3 Renouvellement automatique

```bash
# Tester le renouvellement
certbot renew --dry-run

# Le cron job est automatiquement créé
```

---

## 📊 ÉTAPE 7 : Monitoring et Logs

### 7.1 Voir les logs en temps réel

```bash
# Logs de l'API
docker logs -f fiche-api-prod

# Logs de la base de données
docker logs -f fiche-db-prod

# Logs Nginx
tail -f /var/log/nginx/fiche-api-access.log
tail -f /var/log/nginx/fiche-api-error.log
```

### 7.2 Script de monitoring (optionnel)

Créez `/home/deployer/monitor.sh` :

```bash
#!/bin/bash

echo "=== État des conteneurs ==="
docker ps

echo -e "\n=== Utilisation des ressources ==="
docker stats --no-stream

echo -e "\n=== Espace disque ==="
df -h

echo -e "\n=== Derniers logs API (20 lignes) ==="
docker logs --tail 20 fiche-api-prod
```

---

## 🎯 ÉTAPE 8 : Premier déploiement

### 8.1 Commit et push

```bash
git add .
git commit -m "feat: Add production deployment configuration"
git push origin main
```

### 8.2 Suivre le déploiement

1. Aller sur GitHub → Actions
2. Voir le workflow en cours
3. Vérifier chaque étape

### 8.3 Vérifier le déploiement

```bash
# API directement
curl http://VOTRE_IP:8000/

# Via Nginx (si configuré)
curl http://api.fb-menuiseries.fr/

# Swagger
open http://api.fb-menuiseries.fr/docs
```

---

## 🔧 ÉTAPE 9 : Commandes utiles

### Sur le VPS

```bash
# Redémarrer l'API
cd ~/apps/fiche-api
docker compose -f docker-compose.production.yml restart api

# Voir les logs
docker logs -f fiche-api-prod

# Accéder à la base de données
docker exec -it fiche-db-prod psql -U ficheuser -d fichecontact

# Sauvegarder la base de données
docker exec fiche-db-prod pg_dump -U ficheuser fichecontact > backup-$(date +%Y%m%d).sql

# Restaurer la base de données
docker exec -i fiche-db-prod psql -U ficheuser fichecontact < backup.sql
```

### Rollback

```bash
# Revenir à une version précédente
export IMAGE_TAG="main-abc123"  # SHA du commit précédent
./deploy.sh $IMAGE_TAG
```

---

## 📋 Checklist de déploiement

- [ ] VPS configuré avec Docker
- [ ] Utilisateur `deployer` créé
- [ ] Clés SSH configurées
- [ ] Secrets GitHub ajoutés
- [ ] Workflow CI/CD modifié
- [ ] Premier déploiement réussi
- [ ] Nginx configuré (optionnel)
- [ ] SSL activé (optionnel)
- [ ] Monitoring en place
- [ ] Sauvegardes configurées

---

## 🆘 Dépannage

### Problème : Connexion SSH refuse

```bash
# Sur le VPS, vérifier le service SSH
systemctl status sshd

# Vérifier les logs
tail -f /var/log/auth.log
```

### Problème : Docker ne démarre pas

```bash
# Vérifier les logs
docker logs fiche-api-prod

# Vérifier la configuration
docker compose -f docker-compose.production.yml config
```

### Problème : Base de données inaccessible

```bash
# Vérifier que le conteneur tourne
docker ps | grep fiche-db

# Vérifier les logs
docker logs fiche-db-prod

# Tester la connexion
docker exec -it fiche-db-prod psql -U ficheuser -d fichecontact
```

---

## 🎉 Conclusion

Vous avez maintenant un pipeline CI/CD complet :

1. ✅ Tests automatiques sur chaque commit
2. ✅ Build Docker automatique
3. ✅ Déploiement automatique sur VPS
4. ✅ Reverse proxy Nginx
5. ✅ SSL/HTTPS activé
6. ✅ Monitoring et logs

**Votre API est maintenant en production professionnelle ! 🚀**
