# converters/fiche_converter.py
from typing import List

from contact_fiche.entities.fiche_entity import Fiche
from contact_fiche.entities.works_planned_entity import WorksPlanned
from infrastructure.database.fiche_model import FicheModel, WorkPlannedModel


class FicheConverter:
    @staticmethod
    def model_to_entity(model: FicheModel) -> Fiche:
        wp_list: List[WorksPlanned] = []
        for wp in model.work_planned:
            wp_list.append(WorksPlanned(work=wp.work, details=wp.details))

        return Fiche(
            id=model.id,
            lastname=model.lastname,
            firstname=model.firstname,
            date_rdv=model.date_rdv,
            heure_rdv=model.heure_rdv,
            telephone=model.telephone,
            email=model.email,
            address=model.address,
            code_postal=model.code_postal,
            city=model.city,
            type_logement=model.type_logement,
            statut_habitation=model.statut_habitation,
            origin_contact=model.origin_contact,
            status=model.status,
            commentary=model.commentary,
            works_planned=wp_list,
        )

    @staticmethod
    def entity_to_model(entity: Fiche) -> FicheModel:
        wp_models: List[WorkPlannedModel] = []
        if entity.works_planned:
            for wp in entity.works_planned:
                wp_models.append(WorkPlannedModel(work=wp.work, details=wp.details))

        return FicheModel(
            id=entity.id,
            lastname=entity.lastname,
            firstname=entity.firstname,
            date_rdv=entity.date_rdv,
            heure_rdv=entity.heure_rdv,
            telephone=entity.telephone,
            email=entity.email,
            address=entity.address,
            code_postal=entity.code_postal,
            city=entity.city,
            type_logement=entity.type_logement,
            statut_habitation=entity.statut_habitation,
            origin_contact=entity.origin_contact,
            status=entity.status,
            commentary=entity.commentary,
            work_planned=wp_models,
        )
