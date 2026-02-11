from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import logging
from app.application.dto.parent_dto import ParentCreate, ParentResponse
from app.application.services.register_parent import RegisterParentUseCase
from app.application.services.invite_student import InviteStudentUseCase
from app.infrastructure.repositories.parent_repo_impl import ParentRepositoryImpl
from app.infrastructure.repositories.wallet_repo_impl import WalletRepositoryImpl
from app.infrastructure.repositories.student_repo_impl import StudentRepositoryImpl
from app.infrastructure.database.session import get_db
from app.api.deps import get_current_parent
from app.domain.exceptions import DomainException, UserNotFoundException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/parents", tags=["parents"])

@router.post("/", response_model=ParentResponse)
def register_parent(parent_in: ParentCreate, db: Session = Depends(get_db)):
    """Register a new parent and create their wallet"""
    parent_repo = ParentRepositoryImpl(db)
    wallet_repo = WalletRepositoryImpl(db)
    
    # Check for duplicate email
    existing_parent = parent_repo.get_by_email(parent_in.email)
    if existing_parent:
        raise HTTPException(status_code=400, detail="Parent with this email already exists")
    
    use_case = RegisterParentUseCase(parent_repo=parent_repo, wallet_repo=wallet_repo)
    
    try:
        return use_case.execute(parent_in)
    except DomainException as e:
        logger.error(f"Parent registration failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail="Registration failed. Please try again later.")

@router.post("/invite-student")
def invite_student(student_reg_number: str, current_parent: dict = Depends(get_current_parent), db: Session = Depends(get_db)):
    """Invite a student to link with this parent account"""
    student_repo = StudentRepositoryImpl(db)
    use_case = InviteStudentUseCase(student_repo=student_repo)
    
    try:
        parent_id = UUID(current_parent['id'])
        success = use_case.execute(parent_id, student_reg_number)
        return {"status": "invitation_sent", "student_reg_number": student_reg_number, "confirmed": False}
    except UserNotFoundException as e:
        logger.warning(f"Student not found for invitation: {student_reg_number}")
        raise HTTPException(status_code=404, detail="Student not found")
    except DomainException as e:
        logger.error(f"Student invitation failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Invitation failed. Please try again later.")
