from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.staff import Staff

class StaffRepository(ABC):
    @abstractmethod
    def get_by_id(self, staff_id: UUID) -> Optional[Staff]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Staff]:
        pass

    @abstractmethod
    def save(self, staff: Staff) -> Staff:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Staff]:
        pass

    @abstractmethod
    def delete(self, staff_id: UUID) -> bool:
        pass
