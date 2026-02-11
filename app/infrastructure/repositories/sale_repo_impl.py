from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.sale import Sale, SaleDetail
from app.domain.repositories.sale_repository import SaleRepository

class SaleRepositoryImpl(SaleRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, sale_id: UUID) -> Optional[Sale]:
        return self.db.query(Sale).filter(Sale.id == sale_id).first()

    def get_by_transaction_id(self, transaction_id: str) -> Optional[Sale]:
        return self.db.query(Sale).filter(Sale.transaction_id == transaction_id).first()

    def save(self, sale: Sale) -> Sale:
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Sale]:
        return self.db.query(Sale).offset(skip).limit(limit).all()

    def get_sale_details(self, sale_id: UUID) -> List[SaleDetail]:
        return self.db.query(SaleDetail).filter(SaleDetail.sale_id == sale_id).all()
