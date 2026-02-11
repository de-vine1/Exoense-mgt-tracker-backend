from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_product_repo, get_current_admin
from app.application.dto.product_dto import ProductCreate, ProductUpdate, ProductRead
from app.application.services.products.create_product import create_product_service
from app.application.services.products.update_product import update_product_service
from app.application.services.products.delete_product import delete_product_service
from app.application.services.products.get_product import (
    get_product_by_id_service,
    get_all_products_service,
    get_product_by_code_service
)
from app.domain.repositories.product_repository import ProductRepository

router = APIRouter()

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    *,
    repo: ProductRepository = Depends(get_product_repo),
    product_in: ProductCreate,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Create new product.
    """
    product = get_product_by_code_service(repo, code=product_in.code)
    if product:
        raise HTTPException(
            status_code=400,
            detail="Product with this code already exists.",
        )
    return create_product_service(repo, product_in)

@router.get("/", response_model=List[ProductRead])
def read_products(
    repo: ProductRepository = Depends(get_product_repo),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve products.
    """
    return get_all_products_service(repo, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductRead)
def read_product_by_id(
    product_id: UUID,
    repo: ProductRepository = Depends(get_product_repo)
) -> Any:
    """
    Get product by ID.
    """
    product = get_product_by_id_service(repo, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    *,
    repo: ProductRepository = Depends(get_product_repo),
    product_id: UUID,
    product_in: ProductUpdate,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Update a product.
    """
    product = update_product_service(repo, product_id=product_id, update_data=product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=bool)
def delete_product(
    *,
    repo: ProductRepository = Depends(get_product_repo),
    product_id: UUID,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Delete a product.
    """
    success = delete_product_service(repo, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return success
