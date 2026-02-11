from uuid import UUID
from typing import Optional, List
from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository

def get_product_by_id_service(repo: ProductRepository, product_id: UUID) -> Optional[Product]:
    """Retrieve a product by its ID."""
    return repo.get_by_id(product_id)

def get_all_products_service(repo: ProductRepository, skip: int = 0, limit: int = 100) -> List[Product]:
    """Retrieve a list of all products."""
    return repo.get_all(skip=skip, limit=limit)

def get_product_by_code_service(repo: ProductRepository, code: str) -> Optional[Product]:
    """Retrieve a product by its code."""
    return repo.get_by_code(code)
