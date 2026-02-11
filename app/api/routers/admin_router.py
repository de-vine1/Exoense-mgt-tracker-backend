from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.application.dto.fee_dto import FeeCategoryCreate, FeeCategoryResponse, FeeCreate, FeeResponse
from app.application.dto.admin_dto import AdminCreate, AdminUpdate, AdminResponse
from app.application.services.admin import (
    RegisterAdminUseCase, 
    GetAdminsUseCase, 
    GetAdminByIdUseCase, 
    UpdateAdminUseCase, 
    DeleteAdminUseCase
)
from app.infrastructure.repositories.admin_repo_impl import AdminRepositoryImpl
from app.infrastructure.database.session import get_db
from app.api.deps import get_current_admin
from app.domain.exceptions import DomainException

router = APIRouter(prefix="/admin", tags=["admin"])

# --- Dependency Providers ---

def get_admin_repo(db: Session = Depends(get_db)) -> AdminRepositoryImpl:
    return AdminRepositoryImpl(db)

def get_register_use_case(repo: AdminRepositoryImpl = Depends(get_admin_repo)) -> RegisterAdminUseCase:
    return RegisterAdminUseCase(repo)

def get_get_admins_use_case(repo: AdminRepositoryImpl = Depends(get_admin_repo)) -> GetAdminsUseCase:
    return GetAdminsUseCase(repo)

def get_get_admin_by_id_use_case(repo: AdminRepositoryImpl = Depends(get_admin_repo)) -> GetAdminByIdUseCase:
    return GetAdminByIdUseCase(repo)

def get_update_admin_use_case(repo: AdminRepositoryImpl = Depends(get_admin_repo)) -> UpdateAdminUseCase:
    return UpdateAdminUseCase(repo)

def get_delete_admin_use_case(repo: AdminRepositoryImpl = Depends(get_admin_repo)) -> DeleteAdminUseCase:
    return DeleteAdminUseCase(repo)

# --- Routes ---

@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def register_admin(
    admin_in: AdminCreate, 
    use_case: RegisterAdminUseCase = Depends(get_register_use_case)
):
    """Register a new admin (Currently open for initial setup)"""
    try:
        return use_case.execute(admin_in)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")

@router.get("/", response_model=List[AdminResponse])
def get_admins(
    use_case: GetAdminsUseCase = Depends(get_get_admins_use_case),
    current_admin=Depends(get_current_admin)
):
    """Get all admins"""
    return use_case.execute()

@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin(
    admin_id: UUID, 
    use_case: GetAdminByIdUseCase = Depends(get_get_admin_by_id_use_case),
    current_admin=Depends(get_current_admin)
):
    """Get an admin by ID"""
    try:
        return use_case.execute(admin_id)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{admin_id}", response_model=AdminResponse)
def update_admin(
    admin_id: UUID, 
    admin_in: AdminUpdate, 
    use_case: UpdateAdminUseCase = Depends(get_update_admin_use_case),
    current_admin=Depends(get_current_admin)
):
    """Update an admin"""
    try:
        return use_case.execute(admin_id, admin_in)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: UUID, 
    use_case: DeleteAdminUseCase = Depends(get_delete_admin_use_case),
    current_admin=Depends(get_current_admin)
):
    """Delete an admin"""
    try:
        use_case.execute(admin_id)
        return None
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/fee-categories", response_model=FeeCategoryResponse)
def create_fee_category(category_in: FeeCategoryCreate):
    # This would call CreateFeeCategoryUseCase
    return {"id": "uuid", "name": category_in.name, "description": category_in.description, "created_at": "2024-01-01"}

@router.post("/fees", response_model=FeeResponse)
def create_fee(fee_in: FeeCreate):
    # This would call CreateFeeUseCase
    return {"id": "uuid", "name": fee_in.name, "amount": fee_in.amount, "category_id": fee_in.category_id, "is_active": True}


