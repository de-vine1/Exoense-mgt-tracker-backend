from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass
