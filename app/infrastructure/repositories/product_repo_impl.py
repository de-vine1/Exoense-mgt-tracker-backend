from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository

class ProductRepositoryImpl(ProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_by_code(self, code: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.code == code).first()

    def save(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def delete(self, product_id: UUID) -> bool:
        product = self.get_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False
