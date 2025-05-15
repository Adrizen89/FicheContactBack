import json
from pathlib import Path
from typing import Dict, Any

class WorkSchemaConfigService:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        with open(Path(self.config_path), "r", encoding="utf-8") as file:
            self._config = json.load(file)

    def get_schema(self, work: str) -> Dict[str, Any]:
        return self._config.get(work, {})

    def get_all_schemas(self) -> Dict[str, Any]:
        return self._config
