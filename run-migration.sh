#!/bin/bash
# Script pour exécuter la migration planned_works sur le VPS

echo "🔄 Exécution de la migration planned_works..."

docker exec fiche-db-prod psql -U ficheuser -d fichecontact -c "ALTER TABLE fiche ADD COLUMN IF NOT EXISTS planned_works JSONB DEFAULT '[]'::jsonb;"

if [ $? -eq 0 ]; then
    echo "✅ Migration réussie !"

    # Vérification
    echo "📋 Vérification de la colonne:"
    docker exec fiche-db-prod psql -U ficheuser -d fichecontact -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'fiche' AND column_name = 'planned_works';"
else
    echo "❌ Échec de la migration"
    exit 1
fi
