from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from contact_fiche.enums import Status
from infrastructure.database.fiche_converter import FicheConverter
from infrastructure.database.fiche_model import FicheModel, WorkPlannedModel
from contact_fiche.entities.fiche_entity import Fiche

class SQLiteFicheRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, id: str) -> Optional[Fiche]:
        fiche_model = self.session.query(FicheModel).filter(FicheModel.id == id).first()
        return FicheConverter.model_to_entity(fiche_model) if fiche_model else None

    def save(self, fiche: Fiche) -> None:
        try:
            fiche_model = FicheConverter.entity_to_model(fiche)
            self.session.add(fiche_model)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erreur lors de la sauvegarde de la fiche: {str(e)}")

    def update(self, id: str, fiche: Fiche) -> None:
        try:
            # Récupérer la fiche existante
            fiche_model = self.session.query(FicheModel).filter(FicheModel.id == id).first()
            if not fiche_model:
                raise ValueError(f"Fiche avec l'id {id} non trouvée")

            # Mettre à jour les champs simples
            fiche_model.lastname = fiche.lastname
            fiche_model.firstname = fiche.firstname
            fiche_model.date_rdv = fiche.date_rdv
            fiche_model.heure_rdv = fiche.heure_rdv
            fiche_model.telephone = fiche.telephone
            fiche_model.email = fiche.email
            fiche_model.address = fiche.address
            fiche_model.code_postal = fiche.code_postal
            fiche_model.city = fiche.city
            fiche_model.type_logement = fiche.type_logement
            fiche_model.statut_habitation = fiche.statut_habitation
            fiche_model.origin_contact = fiche.origin_contact
            fiche_model.status = fiche.status
            fiche_model.commentary = fiche.commentary

            # Supprimer les anciens works_planned et ajouter les nouveaux
            if fiche.works_planned:
                # Supprimer les anciens
                self.session.query(WorkPlannedModel).filter(WorkPlannedModel.fiche_id == id).delete()

                # Ajouter les nouveaux
                for wp in fiche.works_planned:
                    wp_model = WorkPlannedModel(
                        fiche_id=id,
                        work=wp.work,
                        details=wp.details
                    )
                    self.session.add(wp_model)

            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erreur lors de la mise à jour de la fiche: {str(e)}")

    def delete(self, id: str) -> None:
        try:
            fiche_model = self.session.query(FicheModel).filter(FicheModel.id == id).first()
            if not fiche_model:
                raise ValueError(f"Fiche avec l'id {id} non trouvée")

            self.session.delete(fiche_model)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erreur lors de la suppression de la fiche: {str(e)}")

    def get_all(self) -> List[Fiche]:
        fiche_models = self.session.query(FicheModel).all()
        return [FicheConverter.model_to_entity(model) for model in fiche_models]

    def get_en_cours(self) -> List[Fiche]:
        fiche_models = (
            self.session.query(FicheModel)
            .filter(FicheModel.status == Status.IN_PROGRESS)
            .all()
        )
        return [FicheConverter.model_to_entity(model) for model in fiche_models]

    def valider_fiche(self, id: str) -> None:
        try:
            fiche_model = self.session.query(FicheModel).filter(FicheModel.id == id).first()
            if not fiche_model:
                raise ValueError(f"Fiche avec l'id {id} non trouvée")

            fiche_model.status = Status.COMPLETED
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Erreur lors de la validation de la fiche: {str(e)}")

