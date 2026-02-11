from fastapi import APIRouter, Depends
from uuid import UUID
from app.application.dto.fee_dto import FeeCategoryCreate, FeeCategoryResponse, FeeCreate, FeeResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/fee-categories", response_model=FeeCategoryResponse)
def create_fee_category(category_in: FeeCategoryCreate):
    # This would call CreateFeeCategoryUseCase
    return {"id": "uuid", "name": category_in.name, "description": category_in.description, "created_at": "2024-01-01"}

@router.post("/fees", response_model=FeeResponse)
def create_fee(fee_in: FeeCreate):
    # This would call CreateFeeUseCase
    return {"id": "uuid", "name": fee_in.name, "amount": fee_in.amount, "category_id": fee_in.category_id, "is_active": True}
