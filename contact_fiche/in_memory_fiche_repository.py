from contact_fiche.entities.fiche_entity import Fiche


class InMemoryFicheRepository:
    def __init__(self) -> None:
        self.fiches = {}

    def save(self, fiche: Fiche) -> None:
        self.fiches[fiche.id] = fiche
    
    def get_by_id(self, id: str) -> Fiche | None:
        return self.fiches.get(id)
    
    def update(self, id: str, fiche: Fiche) -> None:
        self.fiches[id] = fiche
    
    def delete(self, id: str) -> None:
        del self.fiches[id]
