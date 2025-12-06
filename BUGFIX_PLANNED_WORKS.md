# Correction du bug : planned_works non sauvegardés

## 📋 Problème initial

Les `planned_works` cochés lors de la création d'une fiche n'étaient pas sauvegardés ou pas renvoyés par l'API.

**Comportement observé** :
1. ✅ Frontend envoie `planned_works: ['fenetre', 'porte_entree']` lors de POST /fiche
2. ❌ Quand on recharge la fiche, l'API renvoie `planned_works: []` (vide)

## 🔍 Diagnostic

### Confusion entre deux concepts

Il y avait une **confusion architecturale** entre deux champs différents :

| Champ | Type | Quand | Usage |
|-------|------|-------|-------|
| **`planned_works`** | `List[str]` | Création | Pense-bête (checkboxes) |
| **`works_planned`** | `List[WorksPlanned]` | Après création | Détails complets validés |

**Exemple** :
```json
// planned_works (simple, création)
["fenetre", "porte_entree"]

// works_planned (détaillé, après)
[{
  "work": "fenetre",
  "details": {
    "materiau": "PVC",
    "color": "BLANC",
    "hauteur": 150,
    "largeur": 120,
    ...
  }
}]
```

### Cause racine

Le champ `planned_works` :
- ✅ Existait dans la base de données (colonne JSON)
- ❌ N'était PAS défini dans le modèle SQLAlchemy (`FicheModel`)
- ❌ N'était PAS défini dans l'entité Pydantic (`Fiche`)
- ❌ N'était PAS géré par le converter
- ❌ N'était PAS passé au usecase de création

Résultat : Les données envoyées par le frontend étaient **ignorées silencieusement**.

## ✅ Solution appliquée

### 1. Mise à jour du modèle SQLAlchemy

**Fichier** : `infrastructure/database/fiche_model.py`

```python
class FicheModel(Base):
    # ... autres champs ...

    # NOUVEAU : Liste simple des travaux prévus
    planned_works = Column(JSON, default=list, nullable=True)

    # Relation vers les travaux validés avec détails
    work_planned = relationship(
        "WorkPlannedModel", back_populates="fiche", cascade="all, delete-orphan"
    )
```

### 2. Mise à jour de l'entité Pydantic

**Fichier** : `contact_fiche/entities/fiche_entity.py`

```python
class Fiche(BaseModel):
    # ... autres champs ...

    # Liste simple des travaux prévus (pense-bête)
    planned_works: Optional[List[str]] = Field(default_factory=list)

    # Travaux validés avec détails complets
    works_planned: Optional[List[WorksPlanned]] = Field(default_factory=list)
```

### 3. Mise à jour du converter

**Fichier** : `infrastructure/database/fiche_converter.py`

```python
@staticmethod
def model_to_entity(model: FicheModel) -> Fiche:
    return Fiche(
        # ... autres champs ...
        planned_works=model.planned_works or [],
        works_planned=wp_list,
    )

@staticmethod
def entity_to_model(entity: Fiche) -> FicheModel:
    return FicheModel(
        # ... autres champs ...
        planned_works=entity.planned_works or [],
        work_planned=wp_models,
    )
```

### 4. Mise à jour du usecase de création

**Fichier** : `contact_fiche/contact_fiche_usecases.py`

```python
class CreateFicheUsecase(Usecase):
    def __call__(
        self,
        # ... autres paramètres ...
        planned_works: Optional[List[str]] = None,  # NOUVEAU
        works_planned: Optional[List[WorksPlanned]] = None,
    ) -> Fiche:
        planned_works_list = planned_works or []

        fiche = Fiche(
            # ... autres champs ...
            planned_works=planned_works_list,  # NOUVEAU
            works_planned=works_planned_list,
        )
```

### 5. Mise à jour de l'endpoint API

**Fichier** : `infrastructure/api/main.py`

```python
created_fiche = usecase(
    # ... autres paramètres ...
    planned_works=fiche.planned_works,  # NOUVEAU
    works_planned=fiche.works_planned,
)
```

### 6. Migration PostgreSQL

**Fichier** : `migrations/002_add_planned_works_postgres.sql`

```sql
-- Ajoute la colonne si elle n'existe pas (idempotent)
ALTER TABLE fiche ADD COLUMN IF NOT EXISTS planned_works JSONB DEFAULT '[]'::jsonb;

COMMENT ON COLUMN fiche.planned_works IS 'Liste simple des travaux prévus (pense-bête). Ex: ["fenetre", "porte_entree"]';
```

## 🚀 Déploiement

### Étapes à suivre en production

1. **Appliquer la migration SQL**
   ```bash
   ssh user@72.61.109.185
   psql -U adrien -d fichecontact
   \i /path/to/migrations/002_add_planned_works_postgres.sql
   ```

2. **Déployer le code backend**
   ```bash
   # Pull les dernières modifications
   git pull origin main

   # Redémarrer le service
   sudo systemctl restart fiche-api
   ```

3. **Vérifier que ça fonctionne**
   ```bash
   # Créer une fiche de test avec planned_works
   curl -X POST http://72.61.109.185:8000/fiche \
     -H "Content-Type: application/json" \
     -d '{
       "lastname": "Test",
       "firstname": "User",
       "planned_works": ["fenetre", "porte_entree"],
       ...
     }'

   # Récupérer la fiche et vérifier que planned_works est présent
   curl http://72.61.109.185:8000/fiche/{id}
   ```

## 📝 Tests recommandés

### Test 1 : Création avec planned_works
```bash
POST /fiche
{
  "lastname": "Dupont",
  "firstname": "Jean",
  "planned_works": ["fenetre", "porte_entree"],
  ...
}

# Attendu: La fiche est créée avec planned_works = ["fenetre", "porte_entree"]
```

### Test 2 : Récupération
```bash
GET /fiche/{id}

# Attendu:
{
  "id": "...",
  "planned_works": ["fenetre", "porte_entree"],
  "works_planned": [],
  ...
}
```

### Test 3 : Ajout de travaux validés
```bash
PUT /fiche/{id}/travaux
{
  "works_planned": [{
    "work": "fenetre",
    "details": {...}
  }]
}

# Attendu:
# - planned_works reste ["fenetre", "porte_entree"]
# - works_planned contient maintenant les détails
# - status passe à COMPLETED
```

## 📚 Documentation mise à jour

- ✅ `FRONTEND_SPECIFICATIONS.md` : Clarification de la différence entre `planned_works` et `works_planned`
- ✅ `migrations/README.md` : Documentation des migrations
- ✅ Types TypeScript : Ajout de commentaires explicatifs

## ✨ Améliorations futures possibles

1. **Validation** : S'assurer que les valeurs dans `planned_works` correspondent aux types de travaux connus
2. **Migration des données** : Si des anciennes fiches ont des données dans un mauvais format, les migrer
3. **Tests unitaires** : Ajouter des tests pour vérifier la sauvegarde de `planned_works`
4. **Documentation API** : Mettre à jour les exemples Swagger/OpenAPI

## 🎯 Résultat final

Après ce fix :
- ✅ `planned_works` est correctement sauvegardé lors de la création
- ✅ `planned_works` est renvoyé par l'API lors de la récupération
- ✅ `works_planned` continue de fonctionner pour les détails validés
- ✅ Pas de confusion entre les deux concepts
- ✅ Frontend peut afficher les travaux prévus lors de l'édition

---

**Date** : 2025-12-06
**Auteur** : Claude Code
