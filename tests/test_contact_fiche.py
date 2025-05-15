from config.works_schemas_config import WorkSchemaConfigService
from contact_fiche.contact_fiche_usecases import CompletionFicheUsecase, CreateFicheUsecase, DeleteFicheUsecase, OriginContact, UpdateFicheUsecase
from contact_fiche.entities.works_planned_entity import WorksPlanned
from contact_fiche.enums import Status
from contact_fiche.in_memory_fiche_repository import InMemoryFicheRepository
import pytest
from pathlib import Path
import json

@pytest.fixture
def repository():
    return InMemoryFicheRepository()

@pytest.fixture
def config_service() -> WorkSchemaConfigService:
    return WorkSchemaConfigService(config_path="./config/config_works.json")

@pytest.fixture
def new_fiche(repository):
    create_fiche_usecase = CreateFicheUsecase(repository)
    travaux_data = [
        {"work": "Porte", "materials": ["PVC", "ALU"]},
        {"work": "Fenêtre", "materials": ["BOIS"]}
    ]
    return create_fiche_usecase(
        lastname= "Doe", 
        firstname= "John", 
        telephone="012345678",
        email="johndoe@gmail.com",
        address="1 rue de Paris, 75000",
        origin_contact=OriginContact.AFFICHAGE,
        works_planned= travaux_data,
        commentary="Ceci est un commentaire"
        )

@pytest.fixture
def new_fiche_empty_works(repository):
    create_fiche_usecase = CreateFicheUsecase(repository)
    return create_fiche_usecase(
        lastname= "Doe", 
        firstname= "John", 
        telephone="012345678",
        email="johndoe@gmail.com",
        address="1 rue de Paris, 75000",
        origin_contact=OriginContact.AFFICHAGE,
        works_planned= [],
        commentary="Ceci est un commentaire"
        )

@pytest.fixture
def sample_config_file(tmp_path: Path) -> str:
    # Exemple de configuration pour les tests
    data = {
        "fenetre": {
            "fields": [
                {"name": "material_color", "type": "object"},
                {"name": "hauteur", "type": "number"}
            ]
        },
        "porte": {
            "fields": [
                {"name": "hauteur", "type": "number"},
                {"name": "largeur", "type": "number"}
            ]
        }
    }
    config_file = tmp_path / "work_schemas.json"
    config_file.write_text(json.dumps(data))
    return str(config_file)

def test_create_fiche(repository):
    create_usecase = CreateFicheUsecase(repository)
    travaux_data = [
        {"work": "Porte", "materials": ["PVC", "ALU"]},
        {"work": "Fenêtre", "materials": ["BOIS"]}
    ]
    created_fiche = create_usecase(
        lastname= "Doe", 
        firstname= "John", 
        telephone="012345678",
        email="johndoe@gmail.com",
        address="1 rue de Paris, 75000",
        origin_contact=OriginContact.AFFICHAGE,
        works_planned= travaux_data,
        commentary="ceci est un commentaire",
        )

    fetched_fiche = repository.get_by_id(created_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.firstname == "John"
    assert fetched_fiche.lastname == "Doe"
    assert fetched_fiche.status == Status.IN_PROGRESS

   

def test_cant_update_fiche_not_existing(repository):
    update_usecase = UpdateFicheUsecase(repository)
    
    with pytest.raises(ValueError):
        update_usecase("non-existing-id", "new_name")

def test_update_fiche_lastname_only(repository, new_fiche):
    update_usecase = UpdateFicheUsecase(repository)
    updated_fiche = update_usecase(new_fiche.id, new_lastname="new_name")

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.lastname == "new_name"

def test_update_fiche_firstname_only(repository, new_fiche):
    update_usecase = UpdateFicheUsecase(repository)
    updated_fiche = update_usecase(new_fiche.id, new_firstname="new_firstname")

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.firstname == "new_firstname"

def test_update_fiche_telephone_only(repository, new_fiche):
    update_usecase = UpdateFicheUsecase(repository)
    updated_fiche = update_usecase(new_fiche.id, new_tel="9876543210")

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.telephone == "9876543210"   

def test_update_fiche_email_only(repository, new_fiche):
    update_usecase = UpdateFicheUsecase(repository)
    updated_fiche = update_usecase(new_fiche.id, new_email="doejohn@gmail.com")

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.email == "doejohn@gmail.com"   

def test_update_fiche_address_only(repository, new_fiche):
    update_usecase = UpdateFicheUsecase(repository)
    updated_fiche = update_usecase(new_fiche.id, new_address="2 rue de Lyon, 69000 Lyon")

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.address == "2 rue de Lyon, 69000 Lyon"   

def test_update_fiche_origin_only(repository, new_fiche):
    update_fiche_usecase = UpdateFicheUsecase(repository)
    updated_fiche = update_fiche_usecase(new_fiche.id, new_origin= OriginContact.RS)

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.origin_contact == OriginContact.RS

def test_update_fiche_works_planned_only(repository, new_fiche):
    update_fiche_usecase = UpdateFicheUsecase(repository)
    travaux_data = [
        {"work": "Porte", "materials": ["PVC", "ALU"]},
        {"work": "Portail", "materials": ["ALU"]}
    ]
    updated_fiche = update_fiche_usecase(new_fiche.id, new_works_planned= travaux_data)

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert len(fetched_fiche.works_planned) == len(travaux_data)
    for wp, expected in zip(fetched_fiche.works_planned, travaux_data):
        assert wp.work == expected["work"]
        # Pour les matériaux, comparez les valeurs (si Material est un Enum)
        assert [m.value for m in wp.materials] == expected["materials"]

def test_update_fiche_commentary(repository, new_fiche):
    update_fiche_usecase = UpdateFicheUsecase(repository)
    update_fiche_usecase(new_fiche.id, new_commentary= "Nouveau commentaire")

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.commentary == "Nouveau commentaire"

def test_update_fiche_both(repository, new_fiche):
    update_usecase = UpdateFicheUsecase(repository)
    updated_fiche = update_usecase(new_fiche.id, new_lastname="new_name", new_firstname="new_firstname", new_tel="9876543210", new_email="doejohn@gmail.com", new_address="2 rue de Lyon, 69000 Lyon")

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is not None
    assert fetched_fiche.lastname == "new_name"
    assert fetched_fiche.firstname == "new_firstname"
    assert fetched_fiche.telephone == "9876543210"
    assert fetched_fiche.email == "doejohn@gmail.com"
    assert fetched_fiche.address == "2 rue de Lyon, 69000 Lyon"



def test_cant_delete_fiche_not_existing(repository):
    delete_fiche_usecase = DeleteFicheUsecase(repository)

    with pytest.raises(ValueError):
        delete_fiche_usecase("non-existing-id")

def test_delete_fiche(repository, new_fiche):
    delete_fiche_usecase = DeleteFicheUsecase(repository)
    delete_fiche_usecase(new_fiche.id)

    fetched_fiche = repository.get_by_id(new_fiche.id)
    assert fetched_fiche is None


def test_cant_completion_fiche_works_empty(repository, new_fiche_empty_works, config_service):
    completion_fiche_usecase = CompletionFicheUsecase(repository, config_service)

    with pytest.raises(ValueError):
        completion_fiche_usecase(new_fiche_empty_works.id, works_planned={})

def test_cant_completion_fiche_not_found(repository, config_service):
    completion_fiche_usecase = CompletionFicheUsecase(repository, config_service)

    with pytest.raises(ValueError):
        completion_fiche_usecase("id-not-existing", works_planned={"porte":""})


def test_load_config(sample_config_file):
    service = WorkSchemaConfigService(config_path=sample_config_file)
    all_schemas = service.get_all_schemas()

    # On vérifie que la configuration est bien chargée et est un dictionnaire
    assert isinstance(all_schemas, dict)
    assert "fenetre" in all_schemas
    assert "porte" in all_schemas

def test_get_schema_valid_key(sample_config_file):
    service = WorkSchemaConfigService(config_path=sample_config_file)
    fenetre_schema = service.get_schema("fenetre")

    # On s'assure que le schéma retourné est bien un dictionnaire et contient la clé "fields"
    assert isinstance(fenetre_schema, dict)
    assert "fields" in fenetre_schema

def test_get_schema_invalid_key(sample_config_file):
    service = WorkSchemaConfigService(config_path=sample_config_file)
    
    # Pour une clé qui n'existe pas, la méthode doit retourner un dictionnaire vide
    non_existent = service.get_schema("non_existent")
    assert non_existent == {}
