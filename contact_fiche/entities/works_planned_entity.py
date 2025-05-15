from typing import Any, Dict, List
from pydantic import BaseModel
from contact_fiche.enums import Material


class WorksPlanned(BaseModel):
    work: str
    details: Dict[str, Any] 

class FicheCompletionData(BaseModel):
    works_planned: List[Dict[str, Any]]