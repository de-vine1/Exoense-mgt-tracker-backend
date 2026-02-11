from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.parent import Parent

class ParentRepository(ABC):
    @abstractmethod
    def get_by_id(self, parent_id: UUID) -> Optional[Parent]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Parent]:
        pass

    @abstractmethod
    def save(self, parent: Parent) -> Parent:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Parent]:
        pass

    @abstractmethod
    def delete(self, parent_id: UUID) -> bool:
        pass
