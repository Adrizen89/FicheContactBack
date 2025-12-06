-- Migration: Rajouter la colonne planned_works pour les travaux prévus (liste simple)
-- Date: 2025-12-06
-- Description: Ajoute un champ JSONB pour stocker la liste des travaux prévus lors de la création
--              Différent de work_planned qui contient les travaux validés avec détails complets
-- Database: PostgreSQL

-- Ajouter la colonne planned_works comme JSONB array
ALTER TABLE fiche ADD COLUMN IF NOT EXISTS planned_works JSONB DEFAULT '[]'::jsonb;

-- Commentaire pour documentation
COMMENT ON COLUMN fiche.planned_works IS 'Liste simple des travaux prévus (pense-bête). Ex: ["fenetre", "porte_entree"]';

-- Vérification: Lister les colonnes
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fiche';
