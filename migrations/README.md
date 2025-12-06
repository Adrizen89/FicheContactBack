# Migrations de la base de données

## Comment appliquer les migrations

### En production (PostgreSQL sur VPS)

Connectez-vous au VPS et exécutez :

```bash
# Se connecter au VPS
ssh user@72.61.109.185

# Se connecter à PostgreSQL
psql -U adrien -d fichecontact

# Appliquer la migration
\i /path/to/migrations/002_add_planned_works_postgres.sql

# Vérifier que la colonne a été ajoutée
\d fiche
```

### En développement local (SQLite)

```bash
# Appliquer la migration SQLite
sqlite3 infrastructure/database/fiche_contact.db < migrations/002_add_planned_works.sql

# Vérifier
sqlite3 infrastructure/database/fiche_contact.db "PRAGMA table_info(fiche);"
```

## Historique des migrations

### 001_remove_obsolete_columns.sql (2025-12-01)
- ❌ **ERREUR** : Cette migration a été créée par erreur
- Supprimait `planned_works` et `works_details`
- **À NE PAS APPLIQUER EN PRODUCTION**

### 002_add_planned_works_postgres.sql (2025-12-06)
- ✅ Rajoute la colonne `planned_works` (JSONB)
- Cette colonne stocke une liste simple de strings (pense-bête)
- Exemple : `["fenetre", "porte_entree"]`
- Utilise `ADD COLUMN IF NOT EXISTS` pour éviter les erreurs si la colonne existe déjà

## Architecture des données

### `planned_works` (colonne dans `fiche`)
- Type : JSONB (PostgreSQL) ou JSON (SQLite)
- Contenu : Liste simple de strings
- Exemple : `["fenetre", "porte_entree", "volet_roulant"]`
- Rempli : Lors de la **création** de la fiche (checkboxes)
- Usage : **Pense-bête** pour se rappeler quels travaux sont prévus

### `work_planned` (table séparée avec relation)
- Type : Table relationnelle avec foreign key vers `fiche`
- Contenu : Objets complets avec détails validés
- Exemple : `{work: "fenetre", details: {materiau: "PVC", color: "BLANC", hauteur: 150, ...}}`
- Rempli : **APRÈS** la création via `PUT /fiche/{id}/travaux`
- Usage : Travaux **validés** avec tous les détails du formulaire dynamique

## Vérification après migration

```sql
-- PostgreSQL
SELECT planned_works FROM fiche LIMIT 1;

-- Devrait retourner un tableau JSON comme: ["fenetre", "porte_entree"]
```
