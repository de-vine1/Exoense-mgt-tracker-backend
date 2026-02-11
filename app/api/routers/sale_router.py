from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_sale_repo, get_wallet_repo, get_transaction_repo, get_current_admin
from app.application.dto.sale_dto import SaleCreate, SaleRead, SaleDetailRead
from app.application.services.sales.create_sale import create_sale_service
from app.application.services.sales.get_sale import (
    get_sale_by_id_service,
    get_all_sales_service,
    get_sale_details_service
)
from app.domain.repositories.sale_repository import SaleRepository
from app.domain.repositories.wallet_repository import WalletRepository
from app.domain.repositories.transaction_repository import TransactionRepository

router = APIRouter()

@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(
    *,
    sale_repo: SaleRepository = Depends(get_sale_repo),
    wallet_repo: WalletRepository = Depends(get_wallet_repo),
    transaction_repo: TransactionRepository = Depends(get_transaction_repo),
    sale_in: SaleCreate
) -> Any:
    """
    Process a new sale.
    """
    return create_sale_service(sale_repo, wallet_repo, transaction_repo, sale_in)

@router.get("/", response_model=List[SaleRead])
def read_sales(
    repo: SaleRepository = Depends(get_sale_repo),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve sales.
    """
    return get_all_sales_service(repo, skip=skip, limit=limit)

@router.get("/{sale_id}", response_model=SaleRead)
def read_sale_by_id(
    sale_id: UUID,
    repo: SaleRepository = Depends(get_sale_repo)
) -> Any:
    """
    Get sale by ID.
    """
    sale = get_sale_by_id_service(repo, sale_id=sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.get("/{sale_id}/details", response_model=List[SaleDetailRead])
def read_sale_details(
    sale_id: UUID,
    repo: SaleRepository = Depends(get_sale_repo)
) -> Any:
    """
    Get details for a specific sale.
    """
    return get_sale_details_service(repo, sale_id=sale_id)
