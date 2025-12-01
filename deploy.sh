#!/bin/bash

# Script de déploiement pour VPS Hostinger
# Usage: ./deploy.sh [IMAGE_TAG]

set -e  # Arrêter en cas d'erreur

# Couleurs pour les logs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}🚀 Déploiement de Fiche API              ${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"

# Variables d'environnement
export IMAGE_TAG=${1:-latest}
export DB_PASSWORD=${DB_PASSWORD}
export GITHUB_REPOSITORY=${GITHUB_REPOSITORY}

# Vérifications
if [ -z "$DB_PASSWORD" ]; then
    echo -e "${RED}❌ Erreur: DB_PASSWORD non défini${NC}"
    exit 1
fi

if [ -z "$GITHUB_REPOSITORY" ]; then
    echo -e "${RED}❌ Erreur: GITHUB_REPOSITORY non défini${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Version: ${IMAGE_TAG}${NC}"
echo -e "${YELLOW}📍 Repository: ${GITHUB_REPOSITORY}${NC}"
echo ""

# Se déplacer dans le dossier de l'application
APP_DIR="${HOME}/apps/fiche-api"
if [ ! -d "$APP_DIR" ]; then
    echo -e "${YELLOW}⚠️  Création du dossier ${APP_DIR}${NC}"
    mkdir -p "$APP_DIR"
fi

cd "$APP_DIR" || exit 1

# Backup de la base de données avant déploiement
if docker ps | grep -q fiche-db-prod; then
    echo -e "${GREEN}💾 Backup de la base de données...${NC}"
    BACKUP_FILE="backup-$(date +%Y%m%d-%H%M%S).sql"
    docker exec fiche-db-prod pg_dump -U ficheuser fichecontact > "$BACKUP_FILE" 2>/dev/null || true
    if [ -f "$BACKUP_FILE" ]; then
        echo -e "${GREEN}✅ Backup créé: ${BACKUP_FILE}${NC}"
    fi
fi

# Arrêt des conteneurs existants
echo -e "${GREEN}🛑 Arrêt des conteneurs existants...${NC}"
docker compose -f docker-compose.production.yml down || true

# Pull de la nouvelle image
echo -e "${GREEN}📥 Téléchargement de la nouvelle image...${NC}"
docker compose -f docker-compose.production.yml pull

# Démarrage des nouveaux conteneurs
echo -e "${GREEN}🚀 Démarrage des nouveaux conteneurs...${NC}"
docker compose -f docker-compose.production.yml up -d

# Attendre que l'API démarre
echo -e "${YELLOW}⏳ Attente du démarrage de l'API...${NC}"
sleep 10

# Health check
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API démarrée avec succès !${NC}"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -e "${YELLOW}⏳ Tentative ${RETRY_COUNT}/${MAX_RETRIES}...${NC}"
    sleep 3
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ L'API n'a pas démarré correctement${NC}"
    echo -e "${YELLOW}📋 Logs de l'API:${NC}"
    docker logs --tail 50 fiche-api-prod
    exit 1
fi

# Nettoyage des images inutilisées
echo -e "${GREEN}🧹 Nettoyage des images inutilisées...${NC}"
docker image prune -f > /dev/null 2>&1

# Affichage des conteneurs en cours
echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}📊 Conteneurs en cours d'exécution${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Déploiement terminé avec succès !${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📝 Commandes utiles:${NC}"
echo -e "  • Logs API:    docker logs -f fiche-api-prod"
echo -e "  • Logs DB:     docker logs -f fiche-db-prod"
echo -e "  • Restart API: docker compose -f docker-compose.production.yml restart api"
echo -e "  • Stop all:    docker compose -f docker-compose.production.yml down"
echo ""
