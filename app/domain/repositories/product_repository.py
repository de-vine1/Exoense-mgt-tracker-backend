from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        pass

    @abstractmethod
    def delete(self, product_id: UUID) -> bool:
        pass
