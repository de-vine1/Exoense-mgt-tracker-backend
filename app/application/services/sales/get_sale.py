from uuid import UUID
from typing import Optional, List
from app.domain.entities.sale import Sale, SaleDetail
from app.domain.repositories.sale_repository import SaleRepository

def get_sale_by_id_service(repo: SaleRepository, sale_id: UUID) -> Optional[Sale]:
    """Retrieve a sale by its ID."""
    return repo.get_by_id(sale_id)

def get_all_sales_service(repo: SaleRepository, skip: int = 0, limit: int = 100) -> List[Sale]:
    """Retrieve a list of all sales."""
    return repo.get_all(skip=skip, limit=limit)

def get_sale_details_service(repo: SaleRepository, sale_id: UUID) -> List[SaleDetail]:
    """Retrieve all details (items) for a specific sale."""
    return repo.get_sale_details(sale_id)
