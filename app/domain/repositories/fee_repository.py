from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.fee import Fee

class FeeRepository(ABC):
    @abstractmethod
    def get_by_id(self, fee_id: UUID) -> Optional[Fee]:
        pass
    
    @abstractmethod
    def get_by_category_id(self, category_id: UUID) -> List[Fee]:
        pass
    
    @abstractmethod
    def save(self, fee: Fee) -> Fee:
        pass
