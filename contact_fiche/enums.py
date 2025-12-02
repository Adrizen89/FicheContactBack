from enum import Enum


class OriginContact(Enum):
    SALON = "Salon"
    CLIENT = "Ancien client"
    RS = "Réseaux sociaux"
    AFFICHAGE = "Affichage"


class Material(Enum):
    PVC = "PVC"
    BOIS = "BOIS"
    ALU = "ALU"


class Status(Enum):
    DEFAULT = "Default"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
