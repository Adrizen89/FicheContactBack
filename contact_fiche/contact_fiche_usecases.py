from abc import ABC
from typing import Any, Dict, List, Optional
from uuid import uuid4

from jsonschema import ValidationError, validate

from config.works_schemas_config import WorkSchemaConfigService
from contact_fiche.entities.fiche_entity import Fiche
from contact_fiche.entities.works_planned_entity import WorksPlanned
from contact_fiche.enums import OriginContact, Status
from contact_fiche.fiche_repository_protocol import FicheRepository


class Usecase(ABC):
    def __init__(self, repository: FicheRepository):
        self.repository = repository

    def __call__(self, *args, **kwargs): ...


class CreateFicheUsecase(Usecase):
    def __call__(
        self,
        lastname: str,
        firstname: str,
        date_rdv: str,
        heure_rdv: str,
        telephone: str,
        email: str,
        address: str,
        city: str,
        code_postal: str,
        type_logement: str,
        statut_habitation: str,
        commentary: str,
        origin_contact: OriginContact,
        works_planned: Optional[List[WorksPlanned]] = None,
    ) -> Fiche:
        works_planned_list = works_planned or []

        fiche = Fiche(
            id=uuid4().hex,
            lastname=lastname,
            firstname=firstname,
            date_rdv=date_rdv,
            heure_rdv=heure_rdv,
            telephone=telephone,
            email=email,
            address=address,
            city=city,
            code_postal=code_postal,
            type_logement=type_logement,
            statut_habitation=statut_habitation,
            origin_contact=origin_contact,
            works_planned=works_planned_list,
            commentary=commentary,
            status=Status.IN_PROGRESS,
        )

        self.repository.save(fiche)
        return fiche


class UpdateFicheUsecase(Usecase):
    def __call__(
        self,
        id: str,
        new_lastname: Optional[str] = None,
        new_firstname: Optional[str] = None,
        new_date_rdv: Optional[str] = None,
        new_heure_rdv: Optional[str] = None,
        new_tel: Optional[str] = None,
        new_email: Optional[str] = None,
        new_address: Optional[str] = None,
        new_code_postal: Optional[str] = None,
        new_city: Optional[str] = None,
        new_type_logement: Optional[str] = None,
        new_statut_habitation: Optional[str] = None,
        new_origin: Optional[OriginContact] = None,
        new_works_planned: Optional[List[WorksPlanned]] = None,
        new_commentary: Optional[str] = None,
    ) -> Fiche:
        fiche = self.repository.get_by_id(id)

        if fiche is None:
            raise ValueError(f"Fiche with id {id} not found")

        if new_lastname is not None:
            fiche.lastname = new_lastname
        if new_firstname is not None:
            fiche.firstname = new_firstname
        if new_date_rdv is not None:
            fiche.date_rdv = new_date_rdv
        if new_heure_rdv is not None:
            fiche.heure_rdv = new_heure_rdv
        if new_tel is not None:
            fiche.telephone = new_tel
        if new_email is not None:
            fiche.email = new_email
        if new_address is not None:
            fiche.address = new_address
        if new_city is not None:
            fiche.city = new_city
        if new_type_logement is not None:
            fiche.type_logement = new_type_logement
        if new_statut_habitation is not None:
            fiche.statut_habitation = new_statut_habitation
        if new_code_postal is not None:
            fiche.code_postal = new_code_postal
        if new_origin is not None:
            fiche.origin_contact = new_origin
        if new_works_planned is not None:
            fiche.works_planned = new_works_planned
        if new_commentary is not None:
            fiche.commentary = new_commentary

        self.repository.update(id, fiche)
        return fiche


class DeleteFicheUsecase(Usecase):
    def __call__(self, id: str) -> None:
        fiche = self.repository.get_by_id(id)
        if fiche is None:
            raise ValueError(f"Fiche with id {id} not found")
        self.repository.delete(fiche.id)


class ValidateFicheUsecase(Usecase):
    """Use case pour valider une fiche et passer son statut à COMPLETED."""

    def __call__(self, fiche_id: str) -> Fiche:
        fiche = self.repository.get_by_id(fiche_id)
        if fiche is None:
            raise ValueError(f"Fiche with id {fiche_id} not found")

        fiche.status = Status.COMPLETED
        self.repository.update(fiche_id, fiche)
        return fiche


class CompletionFicheUsecase(Usecase):
    def __init__(
        self, repository: FicheRepository, config_service: WorkSchemaConfigService
    ):
        super().__init__(repository)
        self.config_service = config_service

    def __call__(self, fiche_id: str, works_data: List[Dict[str, Any]]) -> Fiche:
        fiche = self.repository.get_by_id(fiche_id)
        if fiche is None:
            raise ValueError("Fiche not found")

        if not works_data:
            raise ValueError("works_data cannot be empty")

        for item in works_data:
            if "work" not in item or "details" not in item:
                raise ValueError("Chaque item doit contenir 'work' et 'details'")
            work_type = item["work"]
            details = item["details"]
            schema = self.config_service.get_schema(work_type)
            if not schema:
                raise ValueError(f"Aucun schéma défini pour le work '{work_type}'")
            try:
                validate(instance=details, schema=schema)
            except ValidationError as e:
                raise ValueError(
                    f"Erreur de validation pour le work '{work_type}': {e.message}"
                )

        # Convertir la liste de dictionnaires en liste d'instances de WorksPlanned
        works_planned_list = [WorksPlanned(**item) for item in works_data]
        fiche.works_planned = (
            works_planned_list  # On assigne la liste d'instances, pas les dictionnaires
        )

        fiche.status = Status.COMPLETED
        self.repository.update(fiche_id, fiche)
        return fiche
