from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.sale import Sale, SaleDetail

class SaleRepository(ABC):
    @abstractmethod
    def get_by_id(self, sale_id: UUID) -> Optional[Sale]:
        pass

    @abstractmethod
    def get_by_transaction_id(self, transaction_id: str) -> Optional[Sale]:
        pass

    @abstractmethod
    def save(self, sale: Sale) -> Sale:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        pass

    @abstractmethod
    def get_sale_details(self, sale_id: UUID) -> List[SaleDetail]:
        pass
