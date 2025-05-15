

from config.works_schemas_config import WorkSchemaConfigService


config_service = WorkSchemaConfigService(config_path="config/config_works.json")

fenetre_schema = config_service.get_schema("fenetre")

print(fenetre_schema)