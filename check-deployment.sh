#!/bin/bash

# Script pour vérifier rapidement l'état du déploiement
# Usage: ./check-deployment.sh VOTRE_IP

VPS_IP=${1}

if [ -z "$VPS_IP" ]; then
    echo "❌ Usage: ./check-deployment.sh VOTRE_IP"
    exit 1
fi

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}🔍 Vérification du déploiement${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""

# 1. Test API Health
echo -e "${YELLOW}1. Test de l'API...${NC}"
if curl -f -s "http://${VPS_IP}:8000/" > /dev/null 2>&1; then
    RESPONSE=$(curl -s "http://${VPS_IP}:8000/")
    echo -e "${GREEN}✅ API accessible${NC}"
    echo "   Réponse: $RESPONSE"
else
    echo -e "${RED}❌ API non accessible${NC}"
fi
echo ""

# 2. Test Swagger
echo -e "${YELLOW}2. Test de la documentation Swagger...${NC}"
if curl -f -s "http://${VPS_IP}:8000/docs" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Swagger accessible${NC}"
    echo "   URL: http://${VPS_IP}:8000/docs"
else
    echo -e "${RED}❌ Swagger non accessible${NC}"
fi
echo ""

# 3. Test ReDoc
echo -e "${YELLOW}3. Test de ReDoc...${NC}"
if curl -f -s "http://${VPS_IP}:8000/redoc" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ ReDoc accessible${NC}"
    echo "   URL: http://${VPS_IP}:8000/redoc"
else
    echo -e "${RED}❌ ReDoc non accessible${NC}"
fi
echo ""

# 4. Test d'une route
echo -e "${YELLOW}4. Test de la route /fiches...${NC}"
FICHES_RESPONSE=$(curl -s "http://${VPS_IP}:8000/fiches")
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Route /fiches accessible${NC}"
    echo "   Nombre de fiches: $(echo $FICHES_RESPONSE | grep -o '\[' | wc -l)"
else
    echo -e "${RED}❌ Route /fiches non accessible${NC}"
fi
echo ""

# 5. Vérification SSH (optionnel)
echo -e "${YELLOW}5. Test de connexion SSH...${NC}"
if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no deployer@${VPS_IP} "echo 'SSH OK'" 2>/dev/null | grep -q "SSH OK"; then
    echo -e "${GREEN}✅ Connexion SSH fonctionnelle${NC}"

    # Vérifier les conteneurs Docker
    echo ""
    echo -e "${YELLOW}6. Vérification des conteneurs Docker...${NC}"
    ssh deployer@${VPS_IP} "docker ps --format 'table {{.Names}}\t{{.Status}}'" 2>/dev/null
else
    echo -e "${YELLOW}⚠️  Connexion SSH non testée (normal si tu n'as pas configuré SSH)${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Vérification terminée !${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📝 Liens rapides :${NC}"
echo "   • API:     http://${VPS_IP}:8000/"
echo "   • Swagger: http://${VPS_IP}:8000/docs"
echo "   • ReDoc:   http://${VPS_IP}:8000/redoc"
echo ""
