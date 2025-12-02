from typing import Any, Dict, List

from pydantic import BaseModel


class WorksPlanned(BaseModel):
    work: str
    details: Dict[str, Any]


class FicheCompletionData(BaseModel):
    works_planned: List[Dict[str, Any]]
