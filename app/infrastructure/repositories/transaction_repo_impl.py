from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.transaction import WalletTransaction
from app.domain.repositories.transaction_repository import TransactionRepository

class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, transaction_id: UUID) -> Optional[WalletTransaction]:
        return self.db.query(WalletTransaction).filter(WalletTransaction.id == transaction_id).first()

    def get_by_transaction_id(self, transaction_id: str) -> Optional[WalletTransaction]:
        return self.db.query(WalletTransaction).filter(WalletTransaction.transaction_id == transaction_id).first()

    def get_by_wallet_id(self, wallet_id: UUID, skip: int = 0, limit: int = 100) -> List[WalletTransaction]:
        return self.db.query(WalletTransaction).filter(WalletTransaction.wallet_id == wallet_id).offset(skip).limit(limit).all()

    def save(self, transaction: WalletTransaction) -> WalletTransaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_all(self, skip: int = 0, limit: int = 100) -> List[WalletTransaction]:
        return self.db.query(WalletTransaction).offset(skip).limit(limit).all()
