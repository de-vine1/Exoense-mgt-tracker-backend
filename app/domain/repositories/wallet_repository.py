from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.wallet import Wallet

class WalletRepository(ABC):
    @abstractmethod
    def get_by_id(self, wallet_id: UUID) -> Optional[Wallet]:
        pass

    @abstractmethod
    def get_all(self) -> List[Wallet]:
        pass
    
    @abstractmethod
    def get_by_student_id(self, student_id: UUID) -> Optional[Wallet]:
        pass
    
    @abstractmethod
    def get_by_parent_id(self, parent_id: UUID) -> Optional[Wallet]:
        pass
    
    @abstractmethod
    def save(self, wallet: Wallet) -> Wallet:
        pass

    @abstractmethod
    def delete(self, wallet_id: UUID) -> bool:
        pass
