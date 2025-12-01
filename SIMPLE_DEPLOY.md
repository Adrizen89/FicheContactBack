# 🚀 Déploiement Ultra-Simplifié (3 étapes)

## Option A : Avec Docker Compose (Recommandé)

### 1. Prépare ton VPS (5 min - une seule fois)

```bash
# Connecte-toi au VPS
ssh root@VOTRE_IP

# Script d'installation automatique
curl -fsSL https://get.docker.com | sh
mkdir -p ~/fiche-api && cd ~/fiche-api
```

### 2. Crée le fichier de configuration

Sur le VPS, crée un fichier `docker-compose.yml` :

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: fichecontact
      POSTGRES_USER: ficheuser
      POSTGRES_PASSWORD: ChangeMe123!
    volumes:
      - ./data:/var/lib/postgresql/data
    restart: always

  api:
    image: python:3.12-slim
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://ficheuser:ChangeMe123!@db:5432/fichecontact
      ENVIRONMENT: production
    volumes:
      - ./app:/app
    working_dir: /app
    command: sh -c "pip install -r requirements.txt && uvicorn infrastructure.api.main:app --host 0.0.0.0 --port 8000"
    depends_on:
      - db
    restart: always
EOF
```

### 3. Déploie ton code

```bash
# Sur le VPS
mkdir -p app
cd app

# Clone ton repo (ou utilise rsync/scp depuis ta machine locale)
git clone https://github.com/TON_USERNAME/tdd_fiche.git .

# Démarre tout
cd ..
docker compose up -d

# Vérifie que ça marche
curl http://localhost:8000/
```

**C'est tout !** Ton API est en ligne sur `http://VOTRE_IP:8000` 🎉

---

## Option B : Script de déploiement en une commande

### Sur ta machine locale

Crée un script `deploy-simple.sh` :

```bash
#!/bin/bash

VPS_IP="VOTRE_IP"
VPS_USER="root"

echo "🚀 Déploiement vers $VPS_IP..."

# Synchronise le code
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' \
  ./ $VPS_USER@$VPS_IP:~/fiche-api/

# Redémarre l'application
ssh $VPS_USER@$VPS_IP << 'EOF'
cd ~/fiche-api
docker compose down
docker compose up -d
echo "✅ Déployé avec succès !"
EOF
```

Utilisation :

```bash
chmod +x deploy-simple.sh
./deploy-simple.sh
```

---

## Option C : Sans Docker (encore plus simple)

Si tu ne veux pas utiliser Docker :

```bash
# Sur le VPS
ssh root@VOTRE_IP

# Installe Python et PostgreSQL
apt update && apt install -y python3.12 python3-pip postgresql

# Configure PostgreSQL
sudo -u postgres psql << EOF
CREATE DATABASE fichecontact;
CREATE USER ficheuser WITH PASSWORD 'ChangeMe123!';
GRANT ALL PRIVILEGES ON DATABASE fichecontact TO ficheuser;
EOF

# Clone et lance l'app
cd ~
git clone https://github.com/TON_USERNAME/tdd_fiche.git
cd tdd_fiche
pip install -r requirements.txt

# Lance l'API en background
export DATABASE_URL="postgresql://ficheuser:ChangeMe123!@localhost/fichecontact"
nohup uvicorn infrastructure.api.main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
```

---

## 🎯 Quelle option choisir ?

| Option | Complexité | Avantages | Inconvénients |
|--------|-----------|-----------|---------------|
| **Render.com** | ⭐ (très simple) | CI/CD automatique, gratuit, SSL inclus | Moins de contrôle |
| **Docker Compose** | ⭐⭐ (simple) | Isolation, reproductible, facile à gérer | Besoin de Docker |
| **Script rsync** | ⭐⭐ (simple) | Déploiement en une commande | Pas de CI/CD |
| **Sans Docker** | ⭐⭐⭐ (moyen) | Pas besoin de Docker | Difficile à maintenir |

---

## 🔄 Pour mettre à jour après le premier déploiement

**Avec Docker Compose** :
```bash
ssh root@VOTRE_IP
cd ~/fiche-api/app
git pull
cd ..
docker compose restart api
```

**Avec le script** :
```bash
./deploy-simple.sh
```

**Sans Docker** :
```bash
ssh root@VOTRE_IP
cd ~/tdd_fiche
git pull
pkill -f uvicorn
nohup uvicorn infrastructure.api.main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
```

---

## 💡 Recommandation

Pour débuter rapidement : **Option A (Docker Compose)**

Pour du long terme : Garde le système CI/CD GitHub Actions que j'ai créé, mais simplifie en :
1. Utilisant un accès par mot de passe au lieu de clés SSH
2. Ou en utilisant GitHub Actions avec un simple `git pull` sur le VPS

Quelle option préfères-tu ?
