# 🎨 Spécifications Frontend - API Fiche Contact

## 📋 Vue d'ensemble du projet

**Objectif** : Application de gestion de fiches clients pour une entreprise de menuiserie (fenêtres, portes, volets, stores).

**Workflow utilisateur** :
1. Création d'une fiche client (contact initial)
2. Fiche passe automatiquement en statut "In Progress"
3. Ajout des détails des travaux validés (avec formulaire dynamique)
4. Validation finale → Fiche "Completed"

**Backend** : FastAPI déployé sur VPS
- URL Production : `http://72.61.109.185:8000`
- Documentation API : `http://72.61.109.185:8000/docs`

---

## 🏗️ Architecture recommandée

### Stack technique

| Technologie | Recommandation | Raison |
|-------------|---------------|--------|
| **Framework** | Vue.js 3 + Composition API | Moderne, performant, TypeScript natif |
| **Langage** | TypeScript | Sécurité des types, meilleure DX |
| **State Management** | Pinia | Plus simple que Vuex, TypeScript natif |
| **Routing** | Vue Router 4 | Standard Vue.js |
| **HTTP Client** | Axios | Intercepteurs, configuration centralisée |
| **UI Library** | Vuetify 3 ou PrimeVue | Composants riches, tableaux puissants |
| **Form Validation** | Vee-Validate + Yup | Validation déclarative |
| **Tests unitaires** | Vitest | Rapide, compatible Vite |
| **Tests E2E** | Cypress ou Playwright | Tests end-to-end |

---

## 📁 Structure du projet

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── client.ts              # Configuration Axios
│   │   └── ficheApi.ts            # Endpoints API
│   │
│   ├── types/
│   │   ├── fiche.types.ts         # Types TypeScript pour Fiche
│   │   ├── works.types.ts         # Types pour WorksPlanned
│   │   └── enums.ts               # Enums (Status, OriginContact, Material)
│   │
│   ├── stores/
│   │   ├── ficheStore.ts          # State management des fiches
│   │   └── worksStore.ts          # State des schémas de travaux
│   │
│   ├── composables/
│   │   ├── useFiche.ts            # Logic réutilisable pour fiches
│   │   └── useWorks.ts            # Logic pour les travaux
│   │
│   ├── components/
│   │   ├── fiche/
│   │   │   ├── FicheCard.vue
│   │   │   ├── FicheForm.vue
│   │   │   ├── FicheList.vue
│   │   │   └── FicheStatusBadge.vue
│   │   │
│   │   ├── works/
│   │   │   ├── WorksFormBuilder.vue  # ⚠️ Composant critique
│   │   │   ├── WorksItemCard.vue
│   │   │   └── WorksTypeSelector.vue
│   │   │
│   │   └── common/
│   │       ├── LoadingSpinner.vue
│   │       ├── ErrorAlert.vue
│   │       └── ConfirmDialog.vue
│   │
│   ├── views/
│   │   ├── DashboardView.vue      # Vue d'ensemble
│   │   ├── FicheListView.vue      # Liste toutes les fiches
│   │   ├── FicheCreateView.vue    # Création nouvelle fiche
│   │   ├── FicheDetailView.vue    # Détails + édition fiche
│   │   └── WorksAddView.vue       # Ajout travaux validés
│   │
│   ├── router/
│   │   └── index.ts
│   │
│   ├── utils/
│   │   ├── formatters.ts          # Formatage dates, prix, etc.
│   │   └── validators.ts          # Validations custom
│   │
│   ├── App.vue
│   └── main.ts
│
├── .env.example
├── vite.config.ts
├── tsconfig.json
└── package.json
```

---

## 🎯 Fonctionnalités principales

### 1. Dashboard (Page d'accueil)

**Route** : `/`

**Contenu** :
```
┌─────────────────────────────────────────┐
│  📊 Statistiques                         │
│  • Total fiches : 42                    │
│  • En cours : 12                        │
│  • Terminées : 30                       │
│  • Villes couvertes : 8                 │
├─────────────────────────────────────────┤
│  📋 Fiches récentes                     │
│  [Liste des 5 dernières fiches]        │
├─────────────────────────────────────────┤
│  ⚡ Actions rapides                     │
│  [+ Nouvelle fiche] [🔍 Rechercher]    │
└─────────────────────────────────────────┘
```

**API utilisées** :
- `GET /fiches` - Toutes les fiches
- `GET /fiches/en-cours` - Fiches en cours
- `GET /fiches/villes` - Liste des villes

**Composants** :
- `DashboardView.vue`
- `StatisticsCard.vue`
- `RecentFichesList.vue`

---

### 2. Liste des fiches

**Route** : `/fiches`

**Fonctionnalités** :
- Tableau avec tri/filtre par colonnes
- Filtres : statut, ville, date
- Recherche par nom/téléphone
- Pagination si > 50 fiches
- Actions : Voir, Éditer, Supprimer

**Colonnes du tableau** :
```
| Nom        | Ville   | Date RDV   | Statut      | Actions    |
|------------|---------|------------|-------------|------------|
| Dupont J.  | Paris   | 15/01/2025 | En cours    | [👁️ ✏️ 🗑️] |
```

**Badges de statut** :
- `DEFAULT` : Badge gris - "Nouvelle"
- `IN_PROGRESS` : Badge orange - "En cours"
- `COMPLETED` : Badge vert - "Terminée"

**API utilisées** :
- `GET /fiches` - Liste complète
- `DELETE /fiche/{id}` - Suppression

**Composants** :
- `FicheListView.vue`
- `FicheCard.vue`
- `FicheStatusBadge.vue`
- `FicheFilters.vue`

---

### 3. Création de fiche (Formulaire multi-étapes)

**Route** : `/fiche/create`

#### Étape 1 : Informations client

**Champs requis** :
- Prénom* (string, min 2 caractères)
- Nom* (string, min 2 caractères)
- Téléphone* (string, format : `^0[1-9]\d{8}$`)
- Email* (email valide)

**Validation** :
```typescript
const schema = yup.object({
  firstname: yup.string().required().min(2),
  lastname: yup.string().required().min(2),
  telephone: yup.string()
    .required()
    .matches(/^0[1-9]\d{8}$/, 'Numéro invalide'),
  email: yup.string().required().email()
})
```

#### Étape 2 : Coordonnées

**Champs requis** :
- Adresse* (string)
- Code postal* (string, 5 chiffres)
- Ville* (string)
- Type logement* (select : Maison, Appartement, Studio, Immeuble)
- Statut habitation* (select : Propriétaire, Locataire, Autre)

#### Étape 3 : Rendez-vous

**Champs requis** :
- Date RDV* (date, format ISO)
- Heure RDV* (time, format HH:MM)
- Origine contact* (select : Salon, Ancien client, Réseaux sociaux, Affichage)
- Travaux prévus (multi-select : fenetre, porte_entree, volet_roulant, etc.)
- Commentaire (textarea, optionnel)

**API utilisée** :
```http
POST /fiche
Content-Type: application/json

{
  "id": "generated-uuid",
  "firstname": "Jean",
  "lastname": "Dupont",
  "date_rdv": "2025-01-15",
  "heure_rdv": "14:00",
  "email": "jean.dupont@mail.com",
  "telephone": "0601020304",
  "address": "10 rue de la Paix",
  "code_postal": "75000",
  "city": "Paris",
  "type_logement": "Maison",
  "statut_habitation": "Propriétaire",
  "origin_contact": "Salon",
  "planned_works": ["fenetre", "porte_entree"],
  "commentary": "Premier contact suite au salon"
}
```

**Réponse** :
- Status 200 : Fiche créée avec statut `IN_PROGRESS`
- Redirection vers `/fiche/{id}`

**Composants** :
- `FicheCreateView.vue`
- `FicheFormStep1.vue`
- `FicheFormStep2.vue`
- `FicheFormStep3.vue`

---

### 4. Détail de la fiche

**Route** : `/fiche/{id}`

**Layout** :
```
┌─────────────────────────────────────────┐
│  Fiche #abc123          [En cours 🟡]   │
│  [✏️ Éditer] [🗑️ Supprimer] [✅ Valider]│
├─────────────────────────────────────────┤
│  👤 Client                              │
│  Jean Dupont                            │
│  📞 0601020304                          │
│  ✉️ jean.dupont@mail.com               │
│  📍 10 rue de la Paix, 75000 Paris     │
│                                         │
│  📅 Rendez-vous                         │
│  15 janvier 2025 à 14h00               │
│  Origine : Salon                       │
│                                         │
│  🔧 Travaux planifiés                  │
│  • Fenêtre                             │
│  • Porte d'entrée                      │
│                                         │
│  💬 Commentaire                         │
│  "Premier contact suite au salon"      │
├─────────────────────────────────────────┤
│  📋 Travaux validés                    │
│  [+ Ajouter des travaux validés]       │
│                                         │
│  [Aucun travail validé pour le moment] │
│  ou                                    │
│  1. Fenêtre Salon - PVC Blanc          │
│     150x120cm - Rénovation             │
│  2. Fenêtre Chambre - ALU Gris         │
│     140x110cm - Neuf                   │
└─────────────────────────────────────────┘
```

**Actions disponibles** :

| Action | Condition | API | Comportement |
|--------|-----------|-----|--------------|
| Éditer | Toujours | `PATCH /fiche/{id}` | Ouvre formulaire de modification |
| Supprimer | Toujours | `DELETE /fiche/{id}` | Confirmation + suppression + redirection |
| Valider | Si `IN_PROGRESS` | `PUT /fiche/{id}/valider` | Passe à `COMPLETED` |
| Ajouter travaux | Si `IN_PROGRESS` | Navigation vers `/fiche/{id}/travaux` | Ouvre formulaire dynamique |

**API utilisées** :
- `GET /fiche/{id}` - Récupérer détails
- `PATCH /fiche/{id}` - Mise à jour partielle
- `DELETE /fiche/{id}` - Suppression
- `PUT /fiche/{id}/valider` - Validation

**Composants** :
- `FicheDetailView.vue`
- `FicheInfo.vue`
- `WorksListCard.vue`

---

### 5. Ajout de travaux validés ⚠️ **FONCTIONNALITÉ CRITIQUE**

**Route** : `/fiche/{id}/travaux`

**⚠️ C'est la partie la plus complexe du frontend !**

#### Workflow complet

##### Étape 1 : Sélection du type de travail

Interface avec boutons/cartes pour choisir :

```
┌─────────────────────────────────────────┐
│  🔧 Ajouter des travaux validés         │
│                                         │
│  Sélectionnez un type de travail :     │
│                                         │
│  [🪟 Fenêtre]     [🚪 Porte d'entrée]  │
│  [🪟 Volet]       [☀️ Store]           │
│  [🚧 Portail]     [🏡 Pergola]         │
│  [🚪 Porte garage] [🏗️ Clôture]        │
│                                         │
└─────────────────────────────────────────┘
```

Types disponibles :
- `fenetre`
- `porte_entree`
- `volet_roulant`
- `volet_battant`
- `store_exterieur`
- `store_interieur`
- `portail`
- `pergola`
- `porte_de_garage`
- `cloture`

##### Étape 2 : Récupération du schéma JSON

**API** :
```http
GET /schema/{work_type}
```

**Exemple de réponse pour `/schema/fenetre`** :
```json
{
  "type": "object",
  "properties": {
    "material_color": {
      "type": "object",
      "properties": {
        "materiau": {
          "type": "string",
          "enum": ["PVC", "BOIS", "ALU"]
        },
        "color": {
          "type": "string",
          "enum": ["BLANC", "GRIS", "NOIR", "MARRON", "BLEU", "VERT", "ROUGE"]
        }
      },
      "required": ["materiau", "color"]
    },
    "choice_piece": {
      "type": "string"
    },
    "type_pose": {
      "type": "string",
      "enum": ["Renovation", "Neuf"]
    },
    "type_window": {
      "type": "string",
      "enum": [
        "Fenetre 1 vantail",
        "Fenetre 2 vantaux",
        "Fenetre 3 vantaux",
        "Porte fenetre 1 vantail",
        "Porte fenetre 2 vantaux"
      ]
    },
    "hauteur": {
      "type": "integer",
      "minimum": 30,
      "maximum": 300
    },
    "largeur": {
      "type": "integer",
      "minimum": 30,
      "maximum": 400
    },
    "allege": {
      "type": "string",
      "enum": ["Oui", "Non"]
    },
    "hab_int": {
      "type": "string",
      "enum": ["Oui", "Non"]
    },
    "hab_ext": {
      "type": "string",
      "enum": ["Oui", "Non"]
    },
    "grille_ventilation": {
      "type": "string",
      "enum": ["Oui", "Non"]
    },
    "commentary": {
      "type": "string"
    }
  },
  "required": [
    "material_color",
    "choice_piece",
    "type_pose",
    "type_window",
    "hauteur",
    "largeur",
    "allege",
    "hab_int",
    "hab_ext",
    "grille_ventilation"
  ]
}
```

##### Étape 3 : Génération dynamique du formulaire

**⚠️ LE FORMULAIRE DOIT ÊTRE 100% DYNAMIQUE BASÉ SUR LE SCHÉMA !**

Le composant `WorksFormBuilder.vue` doit :
1. Parser le schéma JSON
2. Générer les champs appropriés selon le type
3. Gérer la validation
4. Gérer les objets imbriqués (`material_color`)

**Exemple de formulaire généré pour "fenetre"** :
```
┌─────────────────────────────────────────┐
│  🪟 Fenêtre - Détails                   │
│                                         │
│  Matériau* : [PVC ▼]                   │
│  Couleur* : [BLANC ▼]                  │
│                                         │
│  Pièce* : [Salon____________]          │
│                                         │
│  Type de pose* : [Renovation ▼]        │
│  Type de fenêtre* : [Fenetre 2 vantaux ▼]│
│                                         │
│  Dimensions                            │
│  Hauteur (cm)* : [____]                │
│  Largeur (cm)* : [____]                │
│                                         │
│  Allège* : ○ Oui  ● Non                │
│  Habillage intérieur* : ● Oui  ○ Non   │
│  Habillage extérieur* : ○ Oui  ● Non   │
│  Grille ventilation* : ● Oui  ○ Non    │
│                                         │
│  Commentaire / Photo URL :             │
│  [________________________]            │
│                                         │
│  [Annuler] [+ Ajouter un autre] [Valider]│
└─────────────────────────────────────────┘
```

##### Étape 4 : Ajout de plusieurs travaux

L'utilisateur doit pouvoir ajouter plusieurs travaux avant de soumettre :

```
┌─────────────────────────────────────────┐
│  🔧 Travaux à ajouter                   │
│                                         │
│  1. 🪟 Fenêtre - Salon (PVC Blanc)     │
│     150x120cm - Rénovation             │
│     [✏️ Éditer] [🗑️ Supprimer]          │
│                                         │
│  2. 🪟 Fenêtre - Chambre (ALU Gris)    │
│     140x110cm - Neuf                   │
│     [✏️ Éditer] [🗑️ Supprimer]          │
│                                         │
│  [+ Ajouter un autre travail]          │
│  [Annuler]  [Soumettre tout]           │
└─────────────────────────────────────────┘
```

##### Étape 5 : Soumission finale

**API** :
```http
PUT /fiche/{id}/travaux
Content-Type: application/json

{
  "works_planned": [
    {
      "work": "fenetre",
      "details": {
        "material_color": {
          "materiau": "PVC",
          "color": "BLANC"
        },
        "choice_piece": "Salon",
        "type_pose": "Renovation",
        "type_window": "Fenetre 2 vantaux",
        "hauteur": 150,
        "largeur": 120,
        "allege": "Non",
        "hab_int": "Oui",
        "hab_ext": "Non",
        "grille_ventilation": "Oui",
        "commentary": "https://image.com/photo.jpg"
      }
    },
    {
      "work": "fenetre",
      "details": {
        "material_color": {
          "materiau": "ALU",
          "color": "GRIS"
        },
        "choice_piece": "Chambre",
        "type_pose": "Neuf",
        "type_window": "Fenetre 2 vantaux",
        "hauteur": 140,
        "largeur": 110,
        "allege": "Oui",
        "hab_int": "Oui",
        "hab_ext": "Non",
        "grille_ventilation": "Oui",
        "commentary": ""
      }
    }
  ]
}
```

**Réponse** :
- Status 200 : Travaux ajoutés, fiche passe automatiquement à `COMPLETED`
- Status 400 : Validation échouée, retourner les erreurs

**Après succès** :
- Message : "✅ Travaux validés ajoutés avec succès !"
- Redirection vers `/fiche/{id}`
- La fiche affiche maintenant les travaux dans la section "Travaux validés"

**Composants critiques** :
- `WorksAddView.vue`
- `WorksTypeSelector.vue`
- `WorksFormBuilder.vue` ⚠️ **COMPOSANT LE PLUS COMPLEXE**
- `WorksReviewList.vue`

---

## 🎨 Design System

### Palette de couleurs

```css
/* Variables CSS à définir */
:root {
  /* Primary */
  --color-primary: #2563EB;
  --color-primary-dark: #1E40AF;
  --color-primary-light: #60A5FA;

  /* Status */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;
  --color-info: #3B82F6;
  --color-neutral: #6B7280;

  /* Background */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F3F4F6;
  --bg-dark: #111827;

  /* Text */
  --text-primary: #111827;
  --text-secondary: #6B7280;
  --text-light: #9CA3AF;
}
```

### Typography

```css
/* Font sizes */
--text-xs: 0.75rem;   /* 12px */
--text-sm: 0.875rem;  /* 14px */
--text-base: 1rem;    /* 16px */
--text-lg: 1.125rem;  /* 18px */
--text-xl: 1.25rem;   /* 20px */
--text-2xl: 1.5rem;   /* 24px */

/* Font weights */
--font-regular: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Spacing

Utiliser un système cohérent basé sur 8px :
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px

### Responsive breakpoints

```typescript
const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px'
}
```

---

## 🔌 Configuration API

### Variables d'environnement

Créer `.env.example` :
```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
```

### Configuration Axios

**Fichier : `src/api/client.ts`**

```typescript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur pour les requêtes
apiClient.interceptors.request.use(
  config => {
    // Ajouter token si auth
    // const token = localStorage.getItem('token')
    // if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  error => Promise.reject(error)
)

// Intercepteur pour les réponses
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Erreurs HTTP
      switch (error.response.status) {
        case 400:
          console.error('Validation échouée:', error.response.data)
          break
        case 404:
          console.error('Ressource non trouvée')
          break
        case 500:
          console.error('Erreur serveur')
          break
      }
    } else if (error.request) {
      console.error('Pas de réponse du serveur')
    } else {
      console.error('Erreur de configuration:', error.message)
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

### API Endpoints

**Fichier : `src/api/ficheApi.ts`**

```typescript
import apiClient from './client'
import type { Fiche, FicheCompletionData } from '@/types/fiche.types'

export const ficheApi = {
  /**
   * Récupérer toutes les fiches
   */
  getAll: () =>
    apiClient.get<Fiche[]>('/fiches'),

  /**
   * Récupérer une fiche par ID
   */
  getById: (id: string) =>
    apiClient.get<Fiche>(`/fiche/${id}`),

  /**
   * Récupérer les fiches en cours
   */
  getInProgress: () =>
    apiClient.get<Fiche[]>('/fiches/en-cours'),

  /**
   * Récupérer les villes distinctes
   */
  getVilles: () =>
    apiClient.get<string[]>('/fiches/villes'),

  /**
   * Créer une nouvelle fiche
   */
  create: (fiche: Partial<Fiche>) =>
    apiClient.post<Fiche>('/fiche', fiche),

  /**
   * Mettre à jour une fiche (partiel)
   */
  update: (id: string, fiche: Partial<Fiche>) =>
    apiClient.patch<Fiche>(`/fiche/${id}`, fiche),

  /**
   * Valider une fiche (passer à COMPLETED)
   */
  validate: (id: string, fiche: Fiche) =>
    apiClient.put<Fiche>(`/fiche/${id}/valider`, fiche),

  /**
   * Supprimer une fiche
   */
  delete: (id: string) =>
    apiClient.delete(`/fiche/${id}`),

  /**
   * Ajouter des travaux validés à une fiche
   */
  addWorks: (id: string, data: FicheCompletionData) =>
    apiClient.put<Fiche>(`/fiche/${id}/travaux`, data),
}

export const worksApi = {
  /**
   * Récupérer le schéma JSON pour un type de travail
   */
  getSchema: (workType: string) =>
    apiClient.get<any>(`/schema/${workType}`)
}
```

---

## 📦 Types TypeScript

**Fichier : `src/types/fiche.types.ts`**

```typescript
/**
 * ⚠️ IMPORTANT: Différence entre planned_works et works_planned
 *
 * - planned_works: Liste SIMPLE de strings (pense-bête lors de la création)
 *   Exemple: ["fenetre", "porte_entree", "volet_roulant"]
 *   Utilisé dans le formulaire de création (checkboxes) pour se rappeler quels travaux faire
 *
 * - works_planned: Liste d'OBJETS avec détails complets (ajoutés via formulaire dynamique)
 *   Exemple: [{work: "fenetre", details: {materiau: "PVC", color: "BLANC", ...}}]
 *   Ajouté APRÈS la création via PUT /fiche/{id}/travaux
 */

/**
 * Enum pour le statut de la fiche
 */
export enum Status {
  DEFAULT = 'DEFAULT',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED'
}

/**
 * Enum pour l'origine du contact
 */
export enum OriginContact {
  SALON = 'Salon',
  CLIENT = 'Ancien client',
  RS = 'Réseaux sociaux',
  AFFICHAGE = 'Affichage'
}

/**
 * Enum pour les matériaux
 */
export enum Material {
  PVC = 'PVC',
  BOIS = 'BOIS',
  ALU = 'ALU'
}

/**
 * Interface pour un travail planifié avec détails validés
 */
export interface WorksPlanned {
  work: string
  details: Record<string, any>
}

/**
 * Interface principale pour une fiche client
 */
export interface Fiche {
  id: string
  firstname: string
  lastname: string
  date_rdv: string
  heure_rdv: string
  telephone: string
  email: string
  address: string
  code_postal: string
  city: string
  type_logement: string
  statut_habitation: string
  origin_contact: OriginContact
  // Liste simple des travaux prévus (pense-bête) - Ajoutée lors de la création
  planned_works: string[]
  // Travaux validés avec détails complets - Ajoutés via formulaire dynamique
  works_planned: WorksPlanned[]
  commentary: string
  status: Status
}

/**
 * Interface pour l'ajout de travaux validés
 */
export interface FicheCompletionData {
  works_planned: Array<{
    work: string
    details: Record<string, any>
  }>
}

/**
 * Type pour la création d'une fiche (champs optionnels)
 */
export type FicheCreateInput = Omit<Fiche, 'id' | 'status' | 'works_planned'> & {
  id?: string
  // planned_works est inclus (liste simple de strings)
  planned_works: string[]
}

/**
 * Type pour la mise à jour d'une fiche (tous champs optionnels)
 */
export type FicheUpdateInput = Partial<Fiche>
```

---

## 🏪 State Management (Pinia)

**Fichier : `src/stores/ficheStore.ts`**

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ficheApi } from '@/api/ficheApi'
import type { Fiche, FicheCreateInput, FicheUpdateInput, FicheCompletionData } from '@/types/fiche.types'
import { Status } from '@/types/fiche.types'

export const useFicheStore = defineStore('fiche', () => {
  // State
  const fiches = ref<Fiche[]>([])
  const currentFiche = ref<Fiche | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const fichesInProgress = computed(() =>
    fiches.value.filter(f => f.status === Status.IN_PROGRESS)
  )

  const fichesCompleted = computed(() =>
    fiches.value.filter(f => f.status === Status.COMPLETED)
  )

  const fichesDefault = computed(() =>
    fiches.value.filter(f => f.status === Status.DEFAULT)
  )

  const totalFiches = computed(() => fiches.value.length)

  const villes = computed(() => {
    const uniqueVilles = new Set(fiches.value.map(f => f.city))
    return Array.from(uniqueVilles).sort()
  })

  // Actions

  /**
   * Récupérer toutes les fiches
   */
  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const { data } = await ficheApi.getAll()
      fiches.value = data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Récupérer une fiche par ID
   */
  async function fetchById(id: string) {
    loading.value = true
    error.value = null
    try {
      const { data } = await ficheApi.getById(id)
      currentFiche.value = data
      return data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Récupérer les fiches en cours
   */
  async function fetchInProgress() {
    loading.value = true
    error.value = null
    try {
      const { data } = await ficheApi.getInProgress()
      return data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Créer une nouvelle fiche
   */
  async function create(fiche: FicheCreateInput) {
    loading.value = true
    error.value = null
    try {
      const { data } = await ficheApi.create(fiche)
      fiches.value.push(data)
      return data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Mettre à jour une fiche
   */
  async function update(id: string, fiche: FicheUpdateInput) {
    loading.value = true
    error.value = null
    try {
      const { data } = await ficheApi.update(id, fiche)
      const index = fiches.value.findIndex(f => f.id === id)
      if (index !== -1) {
        fiches.value[index] = data
      }
      if (currentFiche.value?.id === id) {
        currentFiche.value = data
      }
      return data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Valider une fiche (passer à COMPLETED)
   */
  async function validate(id: string, fiche: Fiche) {
    loading.value = true
    error.value = null
    try {
      const { data } = await ficheApi.validate(id, fiche)
      const index = fiches.value.findIndex(f => f.id === id)
      if (index !== -1) {
        fiches.value[index] = data
      }
      if (currentFiche.value?.id === id) {
        currentFiche.value = data
      }
      return data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Supprimer une fiche
   */
  async function deleteFiche(id: string) {
    loading.value = true
    error.value = null
    try {
      await ficheApi.delete(id)
      fiches.value = fiches.value.filter(f => f.id !== id)
      if (currentFiche.value?.id === id) {
        currentFiche.value = null
      }
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Ajouter des travaux validés à une fiche
   */
  async function addWorks(id: string, data: FicheCompletionData) {
    loading.value = true
    error.value = null
    try {
      const response = await ficheApi.addWorks(id, data)
      const updatedFiche = response.data

      // Mettre à jour dans la liste
      const index = fiches.value.findIndex(f => f.id === id)
      if (index !== -1) {
        fiches.value[index] = updatedFiche
      }

      // Mettre à jour currentFiche
      if (currentFiche.value?.id === id) {
        currentFiche.value = updatedFiche
      }

      return updatedFiche
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Réinitialiser l'erreur
   */
  function clearError() {
    error.value = null
  }

  return {
    // State
    fiches,
    currentFiche,
    loading,
    error,

    // Getters
    fichesInProgress,
    fichesCompleted,
    fichesDefault,
    totalFiches,
    villes,

    // Actions
    fetchAll,
    fetchById,
    fetchInProgress,
    create,
    update,
    validate,
    deleteFiche,
    addWorks,
    clearError
  }
})
```

**Fichier : `src/stores/worksStore.ts`**

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { worksApi } from '@/api/ficheApi'

export const useWorksStore = defineStore('works', () => {
  // State
  const schemas = ref<Record<string, any>>({})
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Actions

  /**
   * Récupérer le schéma pour un type de travail
   * Mise en cache pour éviter les appels répétés
   */
  async function fetchSchema(workType: string) {
    // Vérifier le cache
    if (schemas.value[workType]) {
      return schemas.value[workType]
    }

    loading.value = true
    error.value = null
    try {
      const { data } = await worksApi.getSchema(workType)
      schemas.value[workType] = data
      return data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Réinitialiser le cache des schémas
   */
  function clearSchemas() {
    schemas.value = {}
  }

  return {
    // State
    schemas,
    loading,
    error,

    // Actions
    fetchSchema,
    clearSchemas
  }
})
```

---

## 🧩 Composants clés

### WorksFormBuilder.vue ⚠️ **COMPOSANT CRITIQUE**

Ce composant génère dynamiquement un formulaire basé sur un schéma JSON.

**Logique de parsing du schéma** :

```typescript
interface FormField {
  name: string
  label: string
  type: 'text' | 'number' | 'select' | 'radio' | 'textarea'
  options?: string[]
  required: boolean
  min?: number
  max?: number
  parent?: string  // Pour les champs imbriqués
}

function parseSchema(
  properties: any,
  required: string[] = [],
  parent: string = ''
): FormField[] {
  const fields: FormField[] = []

  for (const [key, prop] of Object.entries(properties)) {
    const fullKey = parent ? `${parent}.${key}` : key
    const isRequired = required.includes(key)

    if (prop.type === 'object' && prop.properties) {
      // Récursif pour objets imbriqués (ex: material_color)
      fields.push(...parseSchema(
        prop.properties,
        prop.required || [],
        fullKey
      ))
    } else if (prop.enum) {
      // Select ou Radio selon nombre d'options
      fields.push({
        name: fullKey,
        label: formatLabel(key),
        type: prop.enum.length <= 3 ? 'radio' : 'select',
        options: prop.enum,
        required: isRequired
      })
    } else if (prop.type === 'string') {
      fields.push({
        name: fullKey,
        label: formatLabel(key),
        type: 'text',
        required: isRequired
      })
    } else if (prop.type === 'number' || prop.type === 'integer') {
      fields.push({
        name: fullKey,
        label: formatLabel(key),
        type: 'number',
        min: prop.minimum,
        max: prop.maximum,
        required: isRequired
      })
    }
  }

  return fields
}

function formatLabel(key: string): string {
  // Convertir snake_case en format lisible
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
```

**Validation dynamique** :

```typescript
function validateFormData(data: any, schema: any): { valid: boolean, errors: Record<string, string> } {
  const errors: Record<string, string> = {}

  // Vérifier les champs requis
  if (schema.required) {
    for (const field of schema.required) {
      if (!data[field] || (typeof data[field] === 'object' && Object.keys(data[field]).length === 0)) {
        errors[field] = 'Ce champ est requis'
      }
    }
  }

  // Vérifier les types et contraintes
  for (const [key, prop] of Object.entries(schema.properties)) {
    if (data[key] !== undefined) {
      // Vérifier enum
      if (prop.enum && !prop.enum.includes(data[key])) {
        errors[key] = `Valeur invalide. Options: ${prop.enum.join(', ')}`
      }

      // Vérifier min/max pour les nombres
      if (prop.type === 'integer' || prop.type === 'number') {
        if (prop.minimum && data[key] < prop.minimum) {
          errors[key] = `Minimum: ${prop.minimum}`
        }
        if (prop.maximum && data[key] > prop.maximum) {
          errors[key] = `Maximum: ${prop.maximum}`
        }
      }
    }
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors
  }
}
```

---

## ⚠️ Points d'attention critiques

### 1. Formulaire dynamique (WorksFormBuilder)

**Défi** : Générer un formulaire totalement dynamique basé sur un schéma JSON variable.

**Solutions recommandées** :
- Créer un système de composants génériques (`DynamicField.vue`)
- Parser récursivement le schéma JSON
- Gérer les objets imbriqués (`material_color.materiau`, etc.)
- Valider côté client avant soumission
- Gérer les erreurs du backend

**Bibliothèques possibles** :
- `@jsonforms/vue` - Génération de formulaires JSON Schema
- `vue-form-generator` - Générateur de formulaires
- Ou créer le système custom (plus de contrôle)

### 2. Gestion des erreurs API

**Toujours gérer les erreurs 400 (validation)** :

```typescript
try {
  await ficheApi.addWorks(id, data)
  showSuccess('Travaux ajoutés avec succès')
} catch (error: any) {
  if (error.response?.status === 400) {
    const validationErrors = error.response.data.detail
    showError('Validation échouée', validationErrors)
  } else {
    showError('Erreur serveur', error.message)
  }
}
```

### 3. UX - Feedback utilisateur

**Toujours afficher** :
- Loading states (spinners, skeletons)
- Success messages (toasts)
- Error messages (alertes, inline)
- Confirmations avant suppressions

**Exemple avec Vuetify** :
```vue
<v-snackbar v-model="snackbar" :color="snackbarColor">
  {{ snackbarText }}
  <template v-slot:actions>
    <v-btn variant="text" @click="snackbar = false">Fermer</v-btn>
  </template>
</v-snackbar>
```

### 4. Performance

**Optimisations** :
- Lazy loading des vues (`defineAsyncComponent`)
- Pagination de la liste si > 50 fiches
- Debounce sur la recherche (300ms)
- Cache des schémas JSON (ne pas refetch à chaque fois)
- Virtual scrolling si longues listes

**Exemple** :
```typescript
// Lazy loading
const FicheDetailView = defineAsyncComponent(() =>
  import('./views/FicheDetailView.vue')
)

// Debounce
import { useDebounceFn } from '@vueuse/core'

const debouncedSearch = useDebounceFn((query: string) => {
  searchFiches(query)
}, 300)
```

### 5. Validation des données

**Valider AVANT d'envoyer à l'API** :

```typescript
// Utiliser Yup pour la validation
import * as yup from 'yup'

const ficheSchema = yup.object({
  firstname: yup.string().required('Prénom requis').min(2),
  lastname: yup.string().required('Nom requis').min(2),
  telephone: yup.string()
    .required('Téléphone requis')
    .matches(/^0[1-9]\d{8}$/, 'Format invalide (0X XX XX XX XX)'),
  email: yup.string().required('Email requis').email('Email invalide'),
  code_postal: yup.string()
    .required('Code postal requis')
    .matches(/^\d{5}$/, 'Code postal invalide (5 chiffres)')
})

// Dans le composant
const { errors, validate } = useForm({
  validationSchema: ficheSchema
})
```

---

## 🧪 Tests

### Tests unitaires (Vitest)

**Fichier : `src/stores/__tests__/ficheStore.spec.ts`**

```typescript
import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useFicheStore } from '../ficheStore'
import { ficheApi } from '@/api/ficheApi'

vi.mock('@/api/ficheApi')

describe('Fiche Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('devrait récupérer toutes les fiches', async () => {
    const mockFiches = [
      { id: '1', firstname: 'Jean', lastname: 'Dupont', /* ... */ },
      { id: '2', firstname: 'Marie', lastname: 'Martin', /* ... */ }
    ]

    vi.mocked(ficheApi.getAll).mockResolvedValue({ data: mockFiches })

    const store = useFicheStore()
    await store.fetchAll()

    expect(store.fiches).toHaveLength(2)
    expect(store.totalFiches).toBe(2)
  })

  it('devrait créer une nouvelle fiche', async () => {
    const newFiche = {
      firstname: 'Jean',
      lastname: 'Dupont',
      // ...
    }

    const createdFiche = { id: '123', ...newFiche, status: 'IN_PROGRESS' }
    vi.mocked(ficheApi.create).mockResolvedValue({ data: createdFiche })

    const store = useFicheStore()
    const result = await store.create(newFiche)

    expect(result.id).toBe('123')
    expect(store.fiches).toHaveLength(1)
  })

  it('devrait filtrer les fiches en cours', async () => {
    const mockFiches = [
      { id: '1', status: 'IN_PROGRESS', /* ... */ },
      { id: '2', status: 'COMPLETED', /* ... */ },
      { id: '3', status: 'IN_PROGRESS', /* ... */ }
    ]

    vi.mocked(ficheApi.getAll).mockResolvedValue({ data: mockFiches })

    const store = useFicheStore()
    await store.fetchAll()

    expect(store.fichesInProgress).toHaveLength(2)
  })
})
```

### Tests E2E (Cypress)

**Fichier : `cypress/e2e/fiche-creation.cy.ts`**

```typescript
describe('Création de fiche', () => {
  beforeEach(() => {
    cy.visit('/fiche/create')
  })

  it('devrait créer une fiche complète en 3 étapes', () => {
    // Étape 1 : Informations client
    cy.get('[data-test="firstname"]').type('Jean')
    cy.get('[data-test="lastname"]').type('Dupont')
    cy.get('[data-test="telephone"]').type('0601020304')
    cy.get('[data-test="email"]').type('jean.dupont@mail.com')
    cy.get('[data-test="next-btn"]').click()

    // Étape 2 : Coordonnées
    cy.get('[data-test="address"]').type('10 rue de la Paix')
    cy.get('[data-test="code_postal"]').type('75000')
    cy.get('[data-test="city"]').type('Paris')
    cy.get('[data-test="type_logement"]').select('Maison')
    cy.get('[data-test="statut_habitation"]').select('Propriétaire')
    cy.get('[data-test="next-btn"]').click()

    // Étape 3 : Rendez-vous
    cy.get('[data-test="date_rdv"]').type('2025-01-15')
    cy.get('[data-test="heure_rdv"]').type('14:00')
    cy.get('[data-test="origin_contact"]').select('Salon')
    cy.get('[data-test="create-btn"]').click()

    // Vérifications
    cy.url().should('match', /\/fiche\/[a-z0-9-]+/)
    cy.contains('Fiche créée avec succès')
    cy.contains('Jean Dupont')
    cy.contains('En cours')
  })

  it('devrait afficher des erreurs de validation', () => {
    // Essayer de passer à l'étape suivante sans remplir
    cy.get('[data-test="next-btn"]').click()

    cy.contains('Prénom requis')
    cy.contains('Nom requis')
    cy.contains('Téléphone requis')
    cy.contains('Email requis')
  })
})

describe('Ajout de travaux validés', () => {
  beforeEach(() => {
    // Créer une fiche de test
    cy.createTestFiche().then((ficheId) => {
      cy.visit(`/fiche/${ficheId}/travaux`)
    })
  })

  it('devrait ajouter un travail fenêtre', () => {
    // Sélectionner le type
    cy.get('[data-test="work-type-fenetre"]').click()

    // Remplir le formulaire dynamique
    cy.get('[data-test="materiau"]').select('PVC')
    cy.get('[data-test="color"]').select('BLANC')
    cy.get('[data-test="choice_piece"]').type('Salon')
    cy.get('[data-test="type_pose"]').select('Renovation')
    cy.get('[data-test="type_window"]').select('Fenetre 2 vantaux')
    cy.get('[data-test="hauteur"]').type('150')
    cy.get('[data-test="largeur"]').type('120')
    cy.get('[data-test="allege"]').check('Non')
    cy.get('[data-test="hab_int"]').check('Oui')
    cy.get('[data-test="hab_ext"]').check('Non')
    cy.get('[data-test="grille_ventilation"]').check('Oui')

    // Soumettre
    cy.get('[data-test="submit-btn"]').click()

    // Vérifications
    cy.url().should('match', /\/fiche\/[a-z0-9-]+$/)
    cy.contains('Travaux ajoutés avec succès')
    cy.contains('Terminée')
    cy.contains('Fenêtre Salon')
  })
})
```

---

## 📚 Documentation pour le développeur

### Installation et démarrage

```bash
# Cloner le repo
git clone <URL_REPO>
cd frontend

# Installer les dépendances
npm install

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec l'URL de l'API

# Lancer en développement
npm run dev

# Build pour production
npm run build

# Preview du build
npm run preview

# Tests
npm run test        # Tests unitaires
npm run test:e2e    # Tests E2E
npm run lint        # Linting
```

### Structure des commits

Utiliser Conventional Commits :
```
feat: Ajout du formulaire de création de fiche
fix: Correction validation téléphone
refactor: Refactor du composant WorksFormBuilder
docs: Mise à jour README
test: Ajout tests pour ficheStore
chore: Update dependencies
```

### Conventions de nommage

**Composants** : PascalCase
- `FicheCard.vue`
- `WorksFormBuilder.vue`

**Composables** : camelCase avec préfixe `use`
- `useFiche.ts`
- `useWorks.ts`

**Stores** : camelCase avec suffixe `Store`
- `ficheStore.ts`
- `worksStore.ts`

**Types** : PascalCase
- `Fiche`
- `WorksPlanned`

**Fonctions/Variables** : camelCase
- `fetchAll()`
- `currentFiche`

---

## 🎯 Priorités de développement

### Phase 1 - MVP (2-3 semaines) ✅

1. **Setup projet** (1 jour)
   - Init Vue 3 + TypeScript + Vite
   - Config Pinia, Vue Router, Axios
   - Config UI library (Vuetify/PrimeVue)
   - Setup ESLint, Prettier

2. **Types et API** (1 jour)
   - Définir tous les types TypeScript
   - Configuration Axios
   - Création ficheApi et worksApi

3. **Store Pinia** (1 jour)
   - ficheStore avec toutes les actions
   - worksStore pour les schémas

4. **Dashboard** (2 jours)
   - Vue d'ensemble avec stats
   - Liste des fiches récentes

5. **Liste des fiches** (2 jours)
   - Tableau avec tri/filtre
   - Actions (voir, éditer, supprimer)
   - Badges de statut

6. **Création de fiche** (3 jours)
   - Formulaire en 3 étapes
   - Validation avec Vee-Validate
   - Messages de succès/erreur

7. **Détail de fiche** (2 jours)
   - Affichage des informations
   - Actions (éditer, supprimer, valider)

8. **Ajout travaux validés** (5 jours) ⚠️
   - Sélection type de travail
   - Récupération schéma JSON
   - **Composant WorksFormBuilder dynamique**
   - Ajout multiple travaux
   - Soumission

### Phase 2 - Améliorations (1-2 semaines)

1. Recherche avancée
2. Export PDF
3. Statistiques avancées (graphiques)
4. Amélioration UX/UI

### Phase 3 - Nice to have

1. Thème sombre
2. Notifications
3. Historique modifications
4. Upload photos

---

## 🆘 Support et ressources

### Documentation API

- **Swagger** : `http://IP_VPS:8000/docs`
- **ReDoc** : `http://IP_VPS:8000/redoc`

### Ressources Vue.js

- [Vue 3 Docs](https://vuejs.org/)
- [Pinia Docs](https://pinia.vuejs.org/)
- [Vue Router Docs](https://router.vuejs.org/)
- [Vee-Validate Docs](https://vee-validate.logaretm.com/v4/)

### Ressources UI

- [Vuetify 3](https://vuetifyjs.com/)
- [PrimeVue](https://primevue.org/)
- [Tailwind CSS](https://tailwindcss.com/)

### JSON Schema

- [JSON Schema Docs](https://json-schema.org/)
- [Understanding JSON Schema](https://json-schema.org/understanding-json-schema/)

---

## ✅ Checklist finale

Avant de considérer le projet terminé :

### Fonctionnalités
- [ ] Dashboard avec statistiques
- [ ] Liste des fiches avec filtres
- [ ] Création de fiche (3 étapes)
- [ ] Détail de fiche
- [ ] Édition de fiche
- [ ] Suppression de fiche
- [ ] Validation de fiche
- [ ] Ajout travaux validés (formulaire dynamique)

### Qualité
- [ ] Validation de tous les formulaires
- [ ] Gestion erreurs API
- [ ] Messages de feedback (succès/erreur)
- [ ] Loading states
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Tests unitaires (stores)
- [ ] Tests E2E (parcours critiques)

### Performance
- [ ] Lazy loading des vues
- [ ] Cache des schémas JSON
- [ ] Debounce sur recherche
- [ ] Pagination si nécessaire

### Documentation
- [ ] README avec instructions setup
- [ ] Commentaires dans le code
- [ ] Variables d'environnement documentées

---

## 📞 Contact

Pour toute question ou clarification :
- Backend API : Voir documentation Swagger
- Spécifications : Ce document
- Support : [Adresse email ou Slack]

---

**Bon développement ! 🚀**

*Dernière mise à jour : 2025-12-02*
