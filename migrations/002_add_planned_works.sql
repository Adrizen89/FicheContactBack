-- Migration: Rajouter la colonne planned_works pour les travaux prévus (liste simple)
-- Date: 2025-12-06
-- Description: Ajoute un champ JSON pour stocker la liste des travaux prévus lors de la création
--              Différent de work_planned qui contient les travaux validés avec détails complets

-- Ajouter la colonne planned_works comme JSON array
ALTER TABLE fiche ADD COLUMN planned_works TEXT DEFAULT '[]';

-- Note: SQLite stocke JSON comme TEXT
-- Le backend devra parser/serializer ce champ comme une liste de strings
-- Exemple: ["fenetre", "porte_entree", "volet_roulant"]

-- Vérification: Lister les colonnes
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fiche';
