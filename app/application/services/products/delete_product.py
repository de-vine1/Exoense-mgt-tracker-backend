from uuid import UUID
from app.domain.repositories.product_repository import ProductRepository

def delete_product_service(repo: ProductRepository, product_id: UUID) -> bool:
    """
    Delete a product record.
    """
    return repo.delete(product_id)
