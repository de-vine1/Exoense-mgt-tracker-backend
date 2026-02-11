from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.domain.entities.transaction import WalletTransaction

class TransactionRepository(ABC):
    @abstractmethod
    def get_by_id(self, transaction_id: UUID) -> Optional[WalletTransaction]:
        pass

    @abstractmethod
    def get_by_transaction_id(self, transaction_id: str) -> Optional[WalletTransaction]:
        pass

    @abstractmethod
    def get_by_wallet_id(self, wallet_id: UUID, skip: int = 0, limit: int = 100) -> List[WalletTransaction]:
        pass

    @abstractmethod
    def save(self, transaction: WalletTransaction) -> WalletTransaction:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[WalletTransaction]:
        pass
