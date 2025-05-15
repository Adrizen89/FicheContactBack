# converters/fiche_converter.py
from datetime import date
from typing import List, Dict, Any
from infrastructure.database.fiche_model import FicheModel, WorkPlannedModel
from contact_fiche.entities.fiche_entity import Fiche
from contact_fiche.entities.works_planned_entity import WorksPlanned

class FicheConverter:
    @staticmethod
    def model_to_entity(model: FicheModel) -> Fiche:
        wp_list: List[WorksPlanned] = []
        for wp in model.work_planned:
            wp_list.append(WorksPlanned(work=wp.work, details=wp.details))
        return Fiche(
            id=str(model.id),
            lastname=str(model.lastname),
            firstname=str(model.firstname),
            date_rdv=str(model.date_rdv),
            heure_rdv=str(model.heure_rdv),
            telephone=str(model.telephone),
            email=str(model.email),
            address=str(model.address),
            code_postal=str(model.code_postal),
            city=str(model.city),
            type_logement=str(model.type_logement),
            statut_habitation=str(model.statut_habitation),
            origin_contact=model.origin_contact.value,
            status=model.status.value,
            commentary=str(model.commentary),
            planned_works=model.planned_works or [], #type: ignore
            works_details=model.works_details or [], #type: ignore

            works_planned=wp_list
        )
    
    @staticmethod
    def entity_to_model(entity: Fiche) -> FicheModel:
        wp_models: List[WorkPlannedModel] = []
        if entity.works_planned:
            for wp in entity.works_planned:
                wp_models.append(
                    WorkPlannedModel(
                        work=wp.work,
                        details=wp.details
                    )
                )
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
            city= entity.city,
            type_logement=entity.type_logement,
            statut_habitation=entity.statut_habitation,
            origin_contact=entity.origin_contact,
            status=entity.status,                  
            commentary=entity.commentary,
            planned_works=entity.planned_works,
            work_planned=wp_models
        )
