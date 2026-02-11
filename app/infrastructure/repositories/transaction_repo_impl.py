from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import TransactionRepository

class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_by_payer_id(self, payer_id: UUID) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.payer_id == payer_id).all()

    def save(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
