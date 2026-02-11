from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
import logging
from app.application.dto.student_dto import StudentCreate, StudentUpdate, StudentResponse, WalletResponse
from app.application.services.student import (
    RegisterStudentUseCase, 
    InviteStudentUseCase,
    GetStudentsUseCase,
    GetStudentByIdUseCase,
    UpdateStudentUseCase,
    DeleteStudentUseCase
)
from app.application.services.confirm_link import ConfirmLinkUseCase
from app.infrastructure.repositories.student_repo_impl import StudentRepositoryImpl
from app.infrastructure.repositories.wallet_repo_impl import WalletRepositoryImpl
from app.infrastructure.database.session import get_db
from app.api.deps import get_current_student, get_current_admin, get_current_user_data
from app.domain.exceptions import DomainException, UserNotFoundException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["students"])

# --- Dependency Providers ---

def get_student_repo(db: Session = Depends(get_db)) -> StudentRepositoryImpl:
    return StudentRepositoryImpl(db)

def get_wallet_repo(db: Session = Depends(get_db)) -> WalletRepositoryImpl:
    return WalletRepositoryImpl(db)

def get_register_use_case(
    repo: StudentRepositoryImpl = Depends(get_student_repo),
    w_repo: WalletRepositoryImpl = Depends(get_wallet_repo)
) -> RegisterStudentUseCase:
    return RegisterStudentUseCase(repo, w_repo)

def get_get_students_use_case(repo: StudentRepositoryImpl = Depends(get_student_repo)) -> GetStudentsUseCase:
    return GetStudentsUseCase(repo)

def get_get_student_by_id_use_case(repo: StudentRepositoryImpl = Depends(get_student_repo)) -> GetStudentByIdUseCase:
    return GetStudentByIdUseCase(repo)

def get_update_student_use_case(repo: StudentRepositoryImpl = Depends(get_student_repo)) -> UpdateStudentUseCase:
    return UpdateStudentUseCase(repo)

def get_delete_student_use_case(repo: StudentRepositoryImpl = Depends(get_student_repo)) -> DeleteStudentUseCase:
    return DeleteStudentUseCase(repo)

def get_confirm_link_use_case(repo: StudentRepositoryImpl = Depends(get_student_repo)) -> ConfirmLinkUseCase:
    return ConfirmLinkUseCase(repo)

# --- Access Control Helpers ---

def check_student_or_admin(student_id: UUID, user_data: dict = Depends(get_current_user_data)):
    if user_data["role"] == "admin":
        return user_data
    if user_data["role"] == "student" and str(user_data["id"]) == str(student_id):
        return user_data
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this student's data"
    )

# --- Routes ---

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def register_student(
    student_in: StudentCreate, 
    use_case: RegisterStudentUseCase = Depends(get_register_use_case)
):
    """Register a new student and automatically create a wallet"""
    try:
        return use_case.execute(student_in)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Registration failed: {str(e)}")

@router.get("/", response_model=List[StudentResponse])
def get_students(
    use_case: GetStudentsUseCase = Depends(get_get_students_use_case),
    current_admin=Depends(get_current_admin)
):
    """Get all students (Admin only)"""
    return use_case.execute()

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: UUID, 
    use_case: GetStudentByIdUseCase = Depends(get_get_student_by_id_use_case),
    current_user=Depends(check_student_or_admin)
):
    """Get a student by ID (Admin or the student themselves)"""
    try:
        return use_case.execute(student_id)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: UUID, 
    student_in: StudentUpdate, 
    use_case: UpdateStudentUseCase = Depends(get_update_student_use_case),
    current_user=Depends(check_student_or_admin)
):
    """Update a student (Admin or the student themselves)"""
    try:
        return use_case.execute(student_id, student_in)
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: UUID, 
    use_case: DeleteStudentUseCase = Depends(get_delete_student_use_case),
    current_admin=Depends(get_current_admin)
):
    """Delete a student (Admin only)"""
    try:
        use_case.execute(student_id)
        return None
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/confirm-link")
def confirm_parent_link(
    confirm: bool, 
    current_student: dict = Depends(get_current_student), 
    use_case: ConfirmLinkUseCase = Depends(get_confirm_link_use_case)
):
    """Confirm or reject parent link invitation (Student only)"""
    try:
        student_id = UUID(current_student['id'])
        confirmed = use_case.execute(student_id, confirm)
        return {"status": "confirmed" if confirmed else "rejected", "student_id": str(student_id)}
    except UserNotFoundException as e:
        logger.warning(f"Student not found for link confirmation: {str(e)}")
        raise HTTPException(status_code=404, detail="Student not found")
    except DomainException as e:
        logger.error(f"Link confirmation failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Link confirmation failed")

@router.get("/wallet", response_model=WalletResponse)
def get_student_wallet(
    current_student: dict = Depends(get_current_student), 
    wallet_repo: WalletRepositoryImpl = Depends(get_wallet_repo)
):
    """Get student's wallet balance (Student only)"""
    try:
        student_id = UUID(current_student['id'])
        wallet = wallet_repo.get_by_student_id(student_id)
        
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found for this student")
        
        return WalletResponse(
            balance=wallet.balance,
            payer_id=wallet.student_id,
            payer_type="student"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid student ID")

