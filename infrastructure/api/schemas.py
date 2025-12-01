"""
Schémas Pydantic pour l'API.
Séparation entre les modèles de domaine et les DTOs (Data Transfer Objects) de l'API.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from contact_fiche.enums import OriginContact, Status
from contact_fiche.entities.works_planned_entity import WorksPlanned


class FicheCreateRequest(BaseModel):
    """Schéma pour la création d'une fiche."""
    lastname: str = Field(..., min_length=1, max_length=100, description="Nom de famille du client")
    firstname: str = Field(..., min_length=1, max_length=100, description="Prénom du client")
    date_rdv: str = Field(..., description="Date du rendez-vous (format: YYYY-MM-DD)")
    heure_rdv: str = Field(..., description="Heure du rendez-vous (format: HH:MM)")
    telephone: str = Field(..., pattern=r"^0[1-9]\d{8}$", description="Numéro de téléphone français")
    email: EmailStr = Field(..., description="Adresse email du client")
    address: str = Field(..., min_length=1, description="Adresse complète")
    code_postal: str = Field(..., pattern=r"^\d{5}$", description="Code postal (5 chiffres)")
    city: str = Field(..., min_length=1, max_length=100, description="Ville")
    type_logement: str = Field(..., description="Type de logement (Maison, Appartement, etc.)")
    statut_habitation: str = Field(..., description="Statut (Propriétaire, Locataire, etc.)")
    origin_contact: OriginContact = Field(..., description="Origine du contact")
    commentary: str = Field(default="", description="Commentaire libre")
    works_planned: Optional[List[WorksPlanned]] = Field(default_factory=list, description="Travaux planifiés")

    class Config:
        json_schema_extra = {
            "example": {
                "lastname": "Dupont",
                "firstname": "Jean",
                "date_rdv": "2025-01-15",
                "heure_rdv": "14:00",
                "telephone": "0601020304",
                "email": "jean.dupont@email.com",
                "address": "10 rue de la Paix",
                "code_postal": "75000",
                "city": "Paris",
                "type_logement": "Maison",
                "statut_habitation": "Propriétaire",
                "origin_contact": "Salon",
                "commentary": "Premier contact suite au salon"
            }
        }


class FicheUpdateRequest(BaseModel):
    """Schéma pour la mise à jour partielle d'une fiche."""
    lastname: Optional[str] = Field(None, min_length=1, max_length=100)
    firstname: Optional[str] = Field(None, min_length=1, max_length=100)
    date_rdv: Optional[str] = None
    heure_rdv: Optional[str] = None
    telephone: Optional[str] = Field(None, pattern=r"^0[1-9]\d{8}$")
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=1)
    code_postal: Optional[str] = Field(None, pattern=r"^\d{5}$")
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    type_logement: Optional[str] = None
    statut_habitation: Optional[str] = None
    origin_contact: Optional[OriginContact] = None
    commentary: Optional[str] = None
    works_planned: Optional[List[WorksPlanned]] = None


class FicheResponse(BaseModel):
    """Schéma de réponse pour une fiche."""
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
    works_planned: List[WorksPlanned] = Field(default_factory=list)
    commentary: str
    status: Status

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "abc123def456",
                "lastname": "Dupont",
                "firstname": "Jean",
                "date_rdv": "2025-01-15",
                "heure_rdv": "14:00",
                "telephone": "0601020304",
                "email": "jean.dupont@email.com",
                "address": "10 rue de la Paix",
                "code_postal": "75000",
                "city": "Paris",
                "type_logement": "Maison",
                "statut_habitation": "Propriétaire",
                "origin_contact": "Salon",
                "works_planned": [],
                "commentary": "Premier contact",
                "status": "In Progress"
            }
        }


class MessageResponse(BaseModel):
    """Schéma de réponse générique avec message."""
    message: str
    detail: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Opération réussie",
                "detail": "La fiche a été supprimée avec succès"
            }
        }
