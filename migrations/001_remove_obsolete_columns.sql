-- Migration: Supprimer les colonnes obsolètes planned_works et works_details
-- Date: 2025-12-01
-- Description: Ces colonnes ont été remplacées par la relation work_planned

-- Supprimer les colonnes redondantes
ALTER TABLE fiche DROP COLUMN IF EXISTS planned_works;
ALTER TABLE fiche DROP COLUMN IF EXISTS works_details;

-- Vérification: Lister les colonnes restantes
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fiche';
