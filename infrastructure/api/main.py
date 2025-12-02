import logging
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config.works_schemas_config import WorkSchemaConfigService
from contact_fiche.contact_fiche_usecases import (CompletionFicheUsecase,
                                                  CreateFicheUsecase,
                                                  DeleteFicheUsecase,
                                                  UpdateFicheUsecase,
                                                  ValidateFicheUsecase)
from contact_fiche.entities.fiche_entity import Fiche
from contact_fiche.entities.works_planned_entity import (FicheCompletionData,
                                                         WorksPlanned)
from contact_fiche.enums import Status
from infrastructure.database.connexion import get_session
from infrastructure.database.fiche_model import FicheModel
from infrastructure.logging_config import setup_logging
from infrastructure.repositories.sqlite_fiche_repository import \
    SQLiteFicheRepository

# Configuration du logging
setup_logging()
logger = logging.getLogger(__name__)

allowed_origins = ["https://pro-fiche.vercel.app", "http://localhost:5173"]

app = FastAPI(
    title="Fiche API - FB Menuiseries",
    description="API de gestion de fiches clients pour le secteur de la menuiserie",
    version="1.0.0",
    contact={"name": "Adrien", "url": "https://github.com/adrien"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dépendances pour obtenir les instances des repositories et use cases
def get_fiche_repository(db: Session = Depends(get_session)) -> SQLiteFicheRepository:
    return SQLiteFicheRepository(session=db)


def get_create_fiche_usecase(
    repository: SQLiteFicheRepository = Depends(get_fiche_repository),
) -> CreateFicheUsecase:
    return CreateFicheUsecase(repository=repository)


def get_update_fiche_usecase(
    repository: SQLiteFicheRepository = Depends(get_fiche_repository),
) -> UpdateFicheUsecase:
    return UpdateFicheUsecase(repository=repository)


def get_delete_fiche_usecase(
    repository: SQLiteFicheRepository = Depends(get_fiche_repository),
) -> DeleteFicheUsecase:
    return DeleteFicheUsecase(repository=repository)


def get_validate_fiche_usecase(
    repository: SQLiteFicheRepository = Depends(get_fiche_repository),
) -> ValidateFicheUsecase:
    return ValidateFicheUsecase(repository=repository)


def get_completion_fiche_usecase(
    repository: SQLiteFicheRepository = Depends(get_fiche_repository),
) -> CompletionFicheUsecase:
    config_service = WorkSchemaConfigService(config_path="config/config_works.json")
    return CompletionFicheUsecase(repository=repository, config_service=config_service)


def get_config_service():
    return WorkSchemaConfigService(config_path="config/work_schemas.json")


@app.get("/")
def read_root():
    return {"message": "API en ligne ! ✅"}


@app.get("/schema/{work}", response_model=Dict[str, Any])
def get_schema(
    work: str, config_service: WorkSchemaConfigService = Depends(get_config_service)
):
    schema = config_service.get_schema(work)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema


# GET /fiche/{fiche_id} - Récupérer une fiche par son ID
@app.get(
    "/fiche/{fiche_id}",
    response_model=Fiche,
    summary="Récupérer une fiche par ID",
    description="Retourne les détails complets d'une fiche client à partir de son identifiant",
)
def read_fiche(
    fiche_id: str, repository: SQLiteFicheRepository = Depends(get_fiche_repository)
):
    fiche = repository.get_by_id(fiche_id)
    if fiche is None:
        raise HTTPException(status_code=404, detail="Fiche not found")
    return fiche


# GET /fiches/en-cours - Récupérer les fiches en cours
@app.get(
    "/fiches/en-cours",
    response_model=List[Fiche],
    summary="Récupérer les fiches en cours",
    description="Retourne toutes les fiches avec le statut IN_PROGRESS",
)
def read_fiches_en_cours(
    repository: SQLiteFicheRepository = Depends(get_fiche_repository),
):
    fiches = repository.get_en_cours()
    return fiches


# GET /fiches - Récupérer toutes les fiches
@app.get(
    "/fiches",
    response_model=List[Fiche],
    summary="Récupérer toutes les fiches",
    description="Retourne la liste complète de toutes les fiches clients",
)
def read_all_fiches(repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    fiches = repository.get_all()
    return fiches


# POST /fiche - Créer une nouvelle fiche
@app.post(
    "/fiche",
    response_model=Fiche,
    summary="Créer une nouvelle fiche client",
    description="Crée une fiche client avec les informations de contact et passe automatiquement le statut à IN_PROGRESS",
)
def create_fiche(
    fiche: Fiche, usecase: CreateFicheUsecase = Depends(get_create_fiche_usecase)
):
    try:
        logger.info(
            "Creating new fiche",
            extra={
                "lastname": fiche.lastname,
                "firstname": fiche.firstname,
                "origin_contact": fiche.origin_contact.value,
            },
        )
        created_fiche = usecase(
            lastname=fiche.lastname,
            firstname=fiche.firstname,
            date_rdv=fiche.date_rdv,
            heure_rdv=fiche.heure_rdv,
            telephone=fiche.telephone,
            email=fiche.email,
            address=fiche.address,
            city=fiche.city,
            code_postal=fiche.code_postal,
            type_logement=fiche.type_logement,
            statut_habitation=fiche.statut_habitation,
            commentary=fiche.commentary,
            origin_contact=fiche.origin_contact,
            works_planned=fiche.works_planned,
        )
        logger.info("Fiche created successfully", extra={"fiche_id": created_fiche.id})
        return created_fiche
    except Exception as e:
        logger.error("Error creating fiche", extra={"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))


@app.put(
    "/fiche/{fiche_id}/travaux",
    response_model=Fiche,
    summary="Ajouter des travaux validés à une fiche",
    description="Ajoute des travaux avec validation JSON Schema et passe le statut à COMPLETED",
)
def add_travaux_to_fiche(
    fiche_id: str,
    completion_data: FicheCompletionData,
    usecase: CompletionFicheUsecase = Depends(get_completion_fiche_usecase),
):
    try:
        logger.info(
            "Adding works to fiche",
            extra={
                "fiche_id": fiche_id,
                "works_count": len(completion_data.works_planned),
            },
        )
        completed_fiche = usecase(fiche_id, completion_data.works_planned)
        logger.info("Works added successfully", extra={"fiche_id": fiche_id})
        return completed_fiche
    except ValueError as e:
        logger.error(
            "Validation error adding works",
            extra={"fiche_id": fiche_id, "error": str(e)},
        )
        raise HTTPException(status_code=400, detail=str(e))


# PATCH /fiche/{fiche_id} - Mettre à jour partiellement une fiche
@app.patch(
    "/fiche/{fiche_id}",
    response_model=Fiche,
    summary="Mettre à jour une fiche",
    description="Met à jour les champs modifiés d'une fiche existante",
)
def update_fiche(
    fiche_id: str,
    fiche_update: Fiche,
    usecase: UpdateFicheUsecase = Depends(get_update_fiche_usecase),
):
    try:
        updated_fiche = usecase(
            id=fiche_id,
            new_lastname=fiche_update.lastname,
            new_firstname=fiche_update.firstname,
            new_date_rdv=fiche_update.date_rdv,
            new_heure_rdv=fiche_update.heure_rdv,
            new_tel=fiche_update.telephone,
            new_email=fiche_update.email,
            new_address=fiche_update.address,
            new_code_postal=fiche_update.code_postal,
            new_city=fiche_update.city,
            new_type_logement=fiche_update.type_logement,
            new_statut_habitation=fiche_update.statut_habitation,
            new_origin=fiche_update.origin_contact,
            new_works_planned=fiche_update.works_planned,
            new_commentary=fiche_update.commentary,
        )
        return updated_fiche
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# PUT /fiche/{fiche_id}/valider - Mettre le status à valider
@app.put(
    "/fiche/{fiche_id}/valider",
    response_model=Fiche,
    summary="Valider une fiche",
    description="Passe le statut d'une fiche à COMPLETED",
)
def validate_fiche(
    fiche_id: str, usecase: ValidateFicheUsecase = Depends(get_validate_fiche_usecase)
):
    try:
        logger.info("Validating fiche", extra={"fiche_id": fiche_id})
        validated_fiche = usecase(fiche_id)
        logger.info("Fiche validated successfully", extra={"fiche_id": fiche_id})
        return validated_fiche
    except ValueError as e:
        logger.warning("Fiche not found for validation", extra={"fiche_id": fiche_id})
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(
            "Error validating fiche", extra={"fiche_id": fiche_id, "error": str(e)}
        )
        raise HTTPException(status_code=400, detail=str(e))


# DELETE /fiche/{fiche_id} - Supprimer une fiche
@app.delete(
    "/fiche/{fiche_id}",
    summary="Supprimer une fiche",
    description="Supprime définitivement une fiche client de la base de données",
)
def delete_fiche(
    fiche_id: str, usecase: DeleteFicheUsecase = Depends(get_delete_fiche_usecase)
):
    try:
        logger.info("Deleting fiche", extra={"fiche_id": fiche_id})
        usecase(fiche_id)
        logger.info("Fiche deleted successfully", extra={"fiche_id": fiche_id})
        return {"detail": "Fiche deleted"}
    except ValueError as e:
        logger.warning("Fiche not found for deletion", extra={"fiche_id": fiche_id})
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(
            "Error deleting fiche", extra={"fiche_id": fiche_id, "error": str(e)}
        )
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/fiches/villes",
    response_model=List[str],
    summary="Liste des villes distinctes",
    description="Retourne la liste unique de toutes les villes présentes dans les fiches",
)
def get_distinct_cities(db: Session = Depends(get_session)):
    villes = db.query(FicheModel.city).distinct().all()
    return [ville[0] for ville in villes if ville[0]]
