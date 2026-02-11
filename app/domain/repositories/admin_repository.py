from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.admin import Admin

class AdminRepository(ABC):
    @abstractmethod
    def get_by_id(self, admin_id: UUID) -> Optional[Admin]:
        pass

    @abstractmethod
    def get_all(self) -> List[Admin]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Admin]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Admin]:
        pass
    
    @abstractmethod
    def save(self, admin: Admin) -> Admin:
        pass

    @abstractmethod
    def delete(self, admin_id: UUID) -> bool:
        pass

