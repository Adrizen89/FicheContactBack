from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from contact_fiche.entities.works_planned_entity import WorksPlanned
from contact_fiche.enums import OriginContact, Status


class Fiche(BaseModel):
    id: str
    lastname: str
    firstname: str
    date_rdv: str
    heure_rdv: str
    telephone: str
    email: str
    address: str
    code_postal: str
    city: str
    type_logement: str 
    statut_habitation: str
    origin_contact: OriginContact
    planned_works: Optional[List[str]] = []
    works_details: Optional[List[Dict]] = []
    works_planned: Optional[List[WorksPlanned]] = []
    commentary: str
    status: Status = Status.DEFAULT