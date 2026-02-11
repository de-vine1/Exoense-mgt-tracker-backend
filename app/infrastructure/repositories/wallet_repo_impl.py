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

    def get_by_student_id(self, student_id: UUID) -> Optional[Wallet]:
        return self.db.query(Wallet).filter(Wallet.student_id == student_id).first()

    def get_by_parent_id(self, parent_id: UUID) -> Optional[Wallet]:
        return self.db.query(Wallet).filter(Wallet.parent_id == parent_id).first()

    def get_all(self) -> List[Wallet]:
        return self.db.query(Wallet).all()

    def save(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet

    def delete(self, wallet_id: UUID) -> bool:
        wallet = self.get_by_id(wallet_id)
        if wallet:
            self.db.delete(wallet)
            self.db.commit()
            return True
        return False
