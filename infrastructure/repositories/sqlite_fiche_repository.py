from typing import List, Optional
from sqlalchemy.orm import Session

from contact_fiche.enums import Status
from infrastructure.database.fiche_converter import FicheConverter
from infrastructure.database.fiche_model import FicheModel
from contact_fiche.entities.fiche_entity import Fiche

class SQLiteFicheRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: str) -> Optional[Fiche]:
        fiche_model = self.session.query(FicheModel).filter(FicheModel.id == id).first()
        return FicheConverter.model_to_entity(fiche_model) if fiche_model else None

    def save(self, fiche: Fiche) -> None:
        fiche_model = FicheConverter.entity_to_model(fiche)
        self.session.add(fiche_model)
        self.session.commit()

    def update(self, id: str, fiche: Fiche) -> None:

        self.session.query(FicheModel).filter(FicheModel.id == id).update({
            "lastname": fiche.lastname,
            "firstname": fiche.firstname,
            "date_rdv": fiche.date_rdv,
            "heure_rdv": fiche.heure_rdv,
            "telephone": fiche.telephone,
            "email": fiche.email,
            "address": fiche.address,
            "code_postal": fiche.code_postal,
            "city": fiche.city,
            "planned_works": fiche.planned_works,
            "origin_contact": fiche.origin_contact,  
            "status": fiche.status,                  
            "commentary": fiche.commentary,
            "works_details": fiche.works_details,

            
            # Ajoutez ici la gestion des champs complexes comme works_planned ou works_details si nécessaire
        })
        self.session.commit()

    def delete(self, id: str) -> None:
        self.session.query(FicheModel).filter(FicheModel.id == id).delete()
        self.session.commit()

    def get_all(self) -> List[Fiche]:
        fiche_models = self.session.query(FicheModel).all()
        return [FicheConverter.model_to_entity(model) for model in fiche_models]
    
    def get_en_cours(self) -> List[Fiche]:
        results = (
            self.session.query(FicheModel)
            .filter(FicheModel.status == Status.IN_PROGRESS)
            .all()
        )
        return [fiche.to_entity() for fiche in results]
    
    def valider_fiche(self, id: str) -> None:
        self.session.query(FicheModel).filter(FicheModel.id == id).update({
            "status": Status.COMPLETED
        })
        self.session.commit()

