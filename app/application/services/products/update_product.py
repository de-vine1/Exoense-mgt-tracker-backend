from uuid import UUID
from typing import Optional
from app.domain.entities.product import Product
from app.application.dto.product_dto import ProductUpdate
from app.domain.repositories.product_repository import ProductRepository

def update_product_service(repo: ProductRepository, product_id: UUID, update_data: ProductUpdate) -> Optional[Product]:
    """
    Update an existing product's information.
    """
    product = repo.get_by_id(product_id)
    if not product:
        return None
    
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(product, key, value)
            
    return repo.save(product)
