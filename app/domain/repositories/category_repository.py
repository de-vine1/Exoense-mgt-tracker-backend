from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.category import Category

class CategoryRepository(ABC):
    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Category]:
        pass
    
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass
