# 🔐 Configuration des Secrets GitHub

Pour que le déploiement automatique fonctionne, tu dois configurer 4 secrets dans GitHub.

## 📍 Où configurer les secrets ?

Va sur : `https://github.com/Adrizen89/FicheContactBack/settings/secrets/actions`

Ou navigue :
1. Ton repo GitHub
2. **Settings** (onglet en haut)
3. **Secrets and variables** (menu gauche)
4. **Actions**
5. Clique **New repository secret**

---

## 🔑 Les 4 secrets à ajouter

### 1. `VPS_HOST`

**Valeur** : L'adresse IP de ton VPS Hostinger

**Exemple** : `123.45.67.89`

**Comment l'obtenir** :
- Connecte-toi à ton panel Hostinger
- Va dans VPS
- Copie l'adresse IP publique

---

### 2. `VPS_USER`

**Valeur** : `deployer`

**Explication** : C'est le nom de l'utilisateur que le script `setup-vps.sh` crée automatiquement.

---

### 3. `VPS_PASSWORD`

**Valeur** : Le mot de passe que tu as défini pour l'utilisateur `deployer`

**Comment le définir** :
```bash
ssh root@TON_IP
passwd deployer
# Entre ton mot de passe (note-le bien !)
```

⚠️ **Important** : Note ce mot de passe dans un endroit sûr !

---

### 4. `DB_PASSWORD`

**Valeur** : Un mot de passe sécurisé pour PostgreSQL

**Exemple** : `PostgreSQL2025Secure!`

**Conseils** :
- Minimum 12 caractères
- Mélange de lettres, chiffres et symboles
- Ne pas utiliser de caractères spéciaux compliqués (`$`, `` ` ``, `"`, etc.)

---

## ✅ Vérification

Une fois les 4 secrets ajoutés, tu devrais voir :

```
VPS_HOST         Updated now
VPS_USER         Updated now
VPS_PASSWORD     Updated now
DB_PASSWORD      Updated now
```

---

## 🚀 Tester le déploiement

Une fois les secrets configurés :

```bash
git add .
git commit -m "test: Trigger deployment"
git push origin main
```

Puis va sur GitHub → **Actions** et regarde le workflow **Deploy Simple** s'exécuter !

---

## 🆘 En cas d'erreur

### Erreur : "can't connect without a private SSH key or password"

➡️ Le secret `VPS_PASSWORD` n'est pas configuré ou est vide

**Solution** :
1. Vérifie que le secret existe dans GitHub
2. Vérifie qu'il n'y a pas d'espace avant/après le mot de passe

---

### Erreur : "Permission denied"

➡️ Le mot de passe est incorrect

**Solution** :
1. Connecte-toi manuellement pour vérifier : `ssh deployer@TON_IP`
2. Si ça ne marche pas, redéfinis le mot de passe :
   ```bash
   ssh root@TON_IP
   passwd deployer
   ```
3. Mets à jour le secret `VPS_PASSWORD` dans GitHub

---

### Erreur : "Host key verification failed"

➡️ GitHub Actions n'a jamais connecté au VPS avant

**Solution** : Normalement l'action `appleboy/ssh-action` gère ça automatiquement. Si le problème persiste, contacte-moi.

---

## 📝 Note de sécurité

Ces secrets sont **chiffrés** par GitHub et ne sont **jamais exposés** dans les logs.

⚠️ **Ne partage jamais ces secrets** dans les commits, issues, ou discussions publiques !

---

## 🔄 Pour changer un secret plus tard

1. Va sur la page des secrets
2. Clique sur le secret à modifier
3. Entre la nouvelle valeur
4. Clique **Update secret**

Le prochain déploiement utilisera la nouvelle valeur.

---

**Prêt à configurer ?** Suis les étapes ci-dessus ! 🚀
