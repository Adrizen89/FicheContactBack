from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from config.works_schemas_config import WorkSchemaConfigService
from contact_fiche.contact_fiche_usecases import CompletionFicheUsecase
from contact_fiche.entities.fiche_entity import Fiche  
from contact_fiche.entities.works_planned_entity import FicheCompletionData, WorksPlanned
from contact_fiche.enums import Status
from infrastructure.database.connexion import get_session  
from infrastructure.database.fiche_model import FicheModel
from infrastructure.repositories.sqlite_fiche_repository import SQLiteFicheRepository
from fastapi.middleware.cors import CORSMiddleware
import os

allowed_origin = os.getenv("ALLOWED_ORIGIN", "http://localhost:5173")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dépendance pour obtenir une instance du repository de fiche
def get_fiche_repository(db: Session = Depends(get_session)) -> SQLiteFicheRepository:
    return SQLiteFicheRepository(session=db)

def get_completion_fiche_usecase(
    repository: SQLiteFicheRepository = Depends(get_fiche_repository)
) -> CompletionFicheUsecase:
    config_service = WorkSchemaConfigService(config_path="config/config_works.json")
    return CompletionFicheUsecase(repository=repository, config_service=config_service)

def get_config_service():
    return WorkSchemaConfigService(config_path="config/work_schemas.json")

@app.get("/")
def read_root():
    return {"message": "API en ligne ! ✅"}

@app.get("/schema/{work}", response_model=Dict[str, Any])
def get_schema(work: str, config_service: WorkSchemaConfigService = Depends(get_config_service)):
    schema = config_service.get_schema(work)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema

# GET /fiche/{fiche_id} - Récupérer une fiche par son ID
@app.get("/fiche/{fiche_id}", response_model=Fiche)
def read_fiche(fiche_id: str, repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    fiche = repository.get_by_id(fiche_id)
    if fiche is None:
        raise HTTPException(status_code=404, detail="Fiche nott found")
    return fiche

# GET /fiche/en-cours - Récupérer les fiches en cours
@app.get("/fiches/en-cours", response_model=List[Fiche])
def read_fiches(repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    fiches = repository.get_en_cours()
    if fiches is None:
        raise HTTPException(status_code=404, detail="Fiches in progress not found")
    return fiches

# GET /fiche/en-cours - Récupérer les fiches en cours
@app.get("/fiches", response_model=List[Fiche])
def read_all_fiches(repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    fiches = repository.get_all()
    if fiches is None:
        raise HTTPException(status_code=404, detail="Fiches not found")
    return fiches

# POST /fiche - Créer une nouvelle fiche
@app.post("/fiche", response_model=Fiche)
def create_fiche(fiche: Fiche, repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    print(fiche)
    repository.save(fiche)
    return fiche

@app.put("/fiche/{fiche_id}/travaux", response_model=Fiche)
def add_travaux_to_fiche(
    fiche_id: str,
    completion_data: FicheCompletionData,
    usecase: CompletionFicheUsecase = Depends(get_completion_fiche_usecase)
):
    try:
        completed_fiche = usecase(fiche_id, completion_data.works_planned)
        return completed_fiche
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# PATCH /fiche/{fiche_id} - Mettre à jour partiellement une fiche
@app.patch("/fiche/{fiche_id}", response_model=Fiche)
def update_fiche(fiche_id: str, fiche_update: Fiche, repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    print("📥 Fiche reçue en PATCH:", fiche_update)
    repository.update(fiche_id, fiche_update)
    updated_fiche = repository.get_by_id(fiche_id)
    if updated_fiche is None:
        raise HTTPException(status_code=404, detail="Fiche not found after update")
    return updated_fiche

# PUT /fiche/{fiche_id}/valider - Mettre le status à valider
@app.put("/fiche/{fiche_id}/valider", response_model=Fiche)
def update_to_validate(fiche_id: str, fiche_to_update: Fiche, repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    # On met à jour la fiche avec le status à valider
    fiche_to_update.status = Status.COMPLETED
    repository.update(fiche_id, fiche_to_update)
    updated_fiche = repository.get_by_id(fiche_id)
    if updated_fiche is None:
        raise HTTPException(status_code=404, detail="Fiche not found after update")
    return updated_fiche

# DELETE /fiche/{fiche_id} - Supprimer une fiche
@app.delete("/fiche/{fiche_id}")
def delete_fiche(fiche_id: str, repository: SQLiteFicheRepository = Depends(get_fiche_repository)):
    repository.delete(fiche_id)
    return {"detail": "Fiche deleted"}


@app.get("/fiches/villes", response_model=List[str])
def get_distinct_cities(db: Session = Depends(get_session)):
    villes = db.query(FicheModel.city).distinct().all()
    return [ville[0] for ville in villes if ville[0]]



