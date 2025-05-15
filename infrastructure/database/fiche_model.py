from datetime import date
from sqlalchemy import Column, String, Enum as SQLAEnum, ForeignKey, Integer, JSON
from sqlalchemy.orm import declarative_base, relationship
from contact_fiche.entities.fiche_entity import Fiche
from contact_fiche.enums import OriginContact, Status
from infrastructure.database.connexion import get_engine

Base = declarative_base()
engine = get_engine()

class FicheModel(Base):
    __tablename__ = "fiche"

    id = Column(String, primary_key=True)
    lastname = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    date_rdv = Column(String, nullable=False)
    heure_rdv = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    code_postal = Column(String, nullable=False)
    city = Column(String, nullable=False) 
    type_logement = Column(String, nullable=True)
    statut_habitation = Column(String, nullable=True)
    origin_contact = Column(SQLAEnum(OriginContact), nullable=False)
    status = Column(SQLAEnum(Status), default=Status.DEFAULT)
    commentary = Column(String, nullable=True)
    planned_works = Column(JSON, nullable=False, default=list)
    works_details = Column(JSON, nullable=True)
    work_planned = relationship(
        "WorkPlannedModel", back_populates="fiche", cascade="all, delete-orphan"
    )


    def to_entity(self):
        return Fiche(
            id=self.id, # type: ignore
            firstname=self.firstname,# type: ignore
            lastname=self.lastname,# type: ignore
            date_rdv=self.date_rdv,# type: ignore
            heure_rdv=self.heure_rdv,# type: ignore
            email=self.email,# type: ignore
            telephone=self.telephone,# type: ignore
            address=self.address,# type: ignore
            code_postal=self.code_postal,# type: ignore
            city=self.city,# type: ignore
            type_logement=self.type_logement,# type: ignore
            statut_habitation=self.statut_habitation,# type: ignore
            origin_contact=self.origin_contact,# type: ignore
            works_details=self.works_details,  # type: ignore
            status=self.status,# type: ignore
            commentary=self.commentary# type: ignore
        )



class WorkPlannedModel(Base):
    __tablename__ = "work_planned"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fiche_id = Column(String, ForeignKey("fiche.id"), nullable=False)
    work = Column(String, nullable=False)
    # Stocke toutes les données dynamiques validées via vos JSON schemas
    details = Column(JSON, nullable=False)
    
    # Relation inverse vers la fiche
    fiche = relationship("FicheModel", back_populates="work_planned")


Base.metadata.create_all(engine)
