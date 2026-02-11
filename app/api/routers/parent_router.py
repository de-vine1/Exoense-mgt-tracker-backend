from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
import logging
from app.application.dto.parent_dto import ParentCreate, ParentUpdate, ParentResponse
from app.application.dto.student_dto import StudentResponse
from app.application.services.parent import (
    RegisterParentUseCase,
    GetParentsUseCase,
    GetParentByIdUseCase,
    UpdateParentUseCase,
    DeleteParentUseCase
)
from app.application.services.student.invite_student import InviteStudentUseCase
from app.infrastructure.repositories.parent_repo_impl import ParentRepositoryImpl
from app.infrastructure.repositories.student_repo_impl import StudentRepositoryImpl
from app.infrastructure.repositories.wallet_repo_impl import WalletRepositoryImpl
from app.infrastructure.database.session import get_db
from app.api.deps import get_current_parent, get_current_admin, get_current_user_data
from app.domain.exceptions import DomainException, UserNotFoundException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/parents", tags=["parents"])

# --- Dependency Providers ---

def get_parent_repo(db: Session = Depends(get_db)) -> ParentRepositoryImpl:
    return ParentRepositoryImpl(db)

def get_student_repo(db: Session = Depends(get_db)) -> StudentRepositoryImpl:
    return StudentRepositoryImpl(db)

def get_wallet_repo(db: Session = Depends(get_db)) -> WalletRepositoryImpl:
    return WalletRepositoryImpl(db)

def get_register_use_case(
    repo: ParentRepositoryImpl = Depends(get_parent_repo),
    w_repo: WalletRepositoryImpl = Depends(get_wallet_repo)
) -> RegisterParentUseCase:
    return RegisterParentUseCase(repo, w_repo)

def get_get_parents_use_case(repo: ParentRepositoryImpl = Depends(get_parent_repo)) -> GetParentsUseCase:
    return GetParentsUseCase(repo)

def get_get_parent_by_id_use_case(repo: ParentRepositoryImpl = Depends(get_parent_repo)) -> GetParentByIdUseCase:
    return GetParentByIdUseCase(repo)

def get_update_parent_use_case(repo: ParentRepositoryImpl = Depends(get_parent_repo)) -> UpdateParentUseCase:
    return UpdateParentUseCase(repo)

def get_delete_parent_use_case(repo: ParentRepositoryImpl = Depends(get_parent_repo)) -> DeleteParentUseCase:
    return DeleteParentUseCase(repo)

def get_invite_student_use_case(repo: StudentRepositoryImpl = Depends(get_student_repo)) -> InviteStudentUseCase:
    return InviteStudentUseCase(repo)

# --- Access Control Helpers ---

def check_parent_or_admin(parent_id: UUID, user_data: dict = Depends(get_current_user_data)):
    if user_data["role"] == "admin":
        return user_data
    if user_data["role"] == "parent" and str(user_data["id"]) == str(parent_id):
        return user_data
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this parent's data"
    )

# --- Routes ---

@router.post("/", response_model=ParentResponse, status_code=status.HTTP_201_CREATED)
def register_parent(
    parent_in: ParentCreate, 
    use_case: RegisterParentUseCase = Depends(get_register_use_case)
):
    """Register a new parent and create their wallet"""
    try:
        return use_case.execute(parent_in)
    except DomainException as e:
        logger.error(f"Parent registration failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed. Please try again later.")

@router.get("/", response_model=List[ParentResponse])
def get_parents(
    use_case: GetParentsUseCase = Depends(get_get_parents_use_case),
    current_admin=Depends(get_current_admin)
):
    """Get all parents (Admin only)"""
    return use_case.execute()

@router.get("/{parent_id}", response_model=ParentResponse)
def get_parent(
    parent_id: UUID, 
    use_case: GetParentByIdUseCase = Depends(get_get_parent_by_id_use_case),
    current_user=Depends(check_parent_or_admin)
):
    """Get a parent by ID (Admin or the parent themselves)"""
    try:
        return use_case.execute(parent_id)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{parent_id}", response_model=ParentResponse)
def update_parent(
    parent_id: UUID, 
    parent_in: ParentUpdate, 
    use_case: UpdateParentUseCase = Depends(get_update_parent_use_case),
    current_user=Depends(check_parent_or_admin)
):
    """Update a parent (Admin or the parent themselves)"""
    try:
        return use_case.execute(parent_id, parent_in)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{parent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parent(
    parent_id: UUID, 
    use_case: DeleteParentUseCase = Depends(get_delete_parent_use_case),
    current_admin=Depends(get_current_admin)
):
    """Delete a parent (Admin only)"""
    try:
        use_case.execute(parent_id)
        return None
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/invite-student")
def invite_student(
    student_reg_number: str, 
    current_parent: dict = Depends(get_current_parent), 
    use_case: InviteStudentUseCase = Depends(get_invite_student_use_case)
):
    """Invite a student to link with this parent account (Parent only)"""
    try:
        parent_id = UUID(current_parent['id'])
        success = use_case.execute(parent_id, student_reg_number)
        return {"status": "invitation_sent", "student_reg_number": student_reg_number, "confirmed": False}
    except UserNotFoundException as e:
        logger.warning(f"Student not found for invitation: {student_reg_number}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    except DomainException as e:
        logger.error(f"Student invitation failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation failed. Please try again later.")


