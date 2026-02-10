from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        pass
    
    @abstractmethod
    def get_by_payer_id(self, payer_id: UUID) -> List[Transaction]:
        pass
    
    @abstractmethod
    def save(self, transaction: Transaction) -> Transaction:
        pass
