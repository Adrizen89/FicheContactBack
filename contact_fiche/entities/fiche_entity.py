from typing import List, Optional

from pydantic import BaseModel, Field

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
    # Liste simple des travaux prévus (pense-bête) ex: ["fenetre", "porte_entree"]
    planned_works: Optional[List[str]] = Field(default_factory=list)
    # Travaux validés avec détails complets (ajoutés via formulaire dynamique)
    works_planned: Optional[List[WorksPlanned]] = Field(default_factory=list)
    commentary: str
    status: Status = Status.DEFAULT
