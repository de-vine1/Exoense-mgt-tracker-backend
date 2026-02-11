from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.wallet import Wallet
from app.domain.repositories.wallet_repository import WalletRepository

class WalletRepositoryImpl(WalletRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, wallet_id: UUID) -> Optional[Wallet]:
        return self.db.query(Wallet).filter(Wallet.id == wallet_id).first()

    def get_by_code(self, code: str) -> Optional[Wallet]:
        return self.db.query(Wallet).filter(Wallet.code == code).first()

    def get_by_student_id(self, student_id: UUID) -> Optional[Wallet]:
        return self.db.query(Wallet).filter(Wallet.student_id == student_id).first()

    def save(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Wallet]:
        return self.db.query(Wallet).offset(skip).limit(limit).all()
