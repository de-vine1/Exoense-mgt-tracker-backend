from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.fee_category import FeeCategory

class FeeCategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Optional[FeeCategory]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[FeeCategory]:
        pass
    
    @abstractmethod
    def save(self, category: FeeCategory) -> FeeCategory:
        pass
