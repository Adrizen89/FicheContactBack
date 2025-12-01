#!/bin/bash

# Script d'installation VPS pour déploiement GitHub Actions
# Usage: ssh root@VOTRE_IP 'bash -s' < setup-vps.sh

set -e

echo "════════════════════════════════════════"
echo "🚀 Configuration VPS Hostinger"
echo "════════════════════════════════════════"
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Installation Docker
echo -e "${BLUE}📦 Installation de Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✅ Docker installé${NC}"
else
    echo -e "${YELLOW}⚠️  Docker déjà installé${NC}"
fi

# 2. Création utilisateur deployer
echo -e "${BLUE}👤 Création de l'utilisateur deployer...${NC}"
if id "deployer" &>/dev/null; then
    echo -e "${YELLOW}⚠️  L'utilisateur deployer existe déjà${NC}"
else
    useradd -m -s /bin/bash deployer
    echo -e "${GREEN}✅ Utilisateur deployer créé${NC}"
fi

# 3. Configuration sudo
echo -e "${BLUE}🔐 Configuration des permissions...${NC}"
if ! grep -q "deployer ALL=(ALL) NOPASSWD:ALL" /etc/sudoers; then
    echo "deployer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
    echo -e "${GREEN}✅ Permissions sudo configurées${NC}"
else
    echo -e "${YELLOW}⚠️  Permissions sudo déjà configurées${NC}"
fi

# 4. Ajout au groupe docker
usermod -aG docker deployer

# 5. Création du dossier app
echo -e "${BLUE}📁 Création du dossier d'application...${NC}"
su - deployer -c "mkdir -p ~/apps/fiche-api"
echo -e "${GREEN}✅ Dossier créé : /home/deployer/apps/fiche-api${NC}"

# 6. Configuration SSH
echo -e "${BLUE}🔑 Configuration SSH...${NC}"
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd
echo -e "${GREEN}✅ Authentification par mot de passe activée${NC}"

echo ""
echo "════════════════════════════════════════"
echo -e "${GREEN}🎉 Configuration terminée !${NC}"
echo "════════════════════════════════════════"
echo ""
echo -e "${YELLOW}📝 Prochaines étapes :${NC}"
echo ""
echo "1. Définir un mot de passe pour deployer :"
echo "   sudo passwd deployer"
echo ""
echo "2. Tester la connexion :"
echo "   ssh deployer@$(hostname -I | awk '{print $1}')"
echo ""
echo "3. Ajouter les secrets GitHub :"
echo "   VPS_HOST=$(hostname -I | awk '{print $1}')"
echo "   VPS_USER=deployer"
echo "   VPS_PASSWORD=<le_mot_de_passe_que_tu_as_defini>"
echo "   DB_PASSWORD=<un_mot_de_passe_pour_postgresql>"
echo ""
echo -e "${BLUE}📖 Voir DEPLOY_RAPIDE.md pour la suite${NC}"
echo ""
