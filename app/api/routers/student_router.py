from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
import logging
from app.application.dto.student_dto import StudentCreate, StudentResponse, WalletResponse
from app.application.services.register_student import RegisterStudentUseCase
from app.application.services.confirm_link import ConfirmLinkUseCase
from app.infrastructure.repositories.student_repo_impl import StudentRepositoryImpl
from app.infrastructure.repositories.wallet_repo_impl import WalletRepositoryImpl
from app.infrastructure.database.session import get_db
from app.api.deps import get_current_student
from app.domain.exceptions import DomainException, UserNotFoundException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse)
def register_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    """Register a new student and automatically create a wallet"""
    try:
        student_repo = StudentRepositoryImpl(db)
        wallet_repo = WalletRepositoryImpl(db)
        
        # Check if student already exists
        existing_student = student_repo.get_by_reg_number(student_in.reg_number)
        if existing_student:
            raise HTTPException(status_code=400, detail="Student with this registration number already exists")
        
        existing_email = student_repo.get_by_email(student_in.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Student with this email already exists")
        
        use_case = RegisterStudentUseCase(student_repo, wallet_repo)
        result = use_case.execute(student_in)
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/confirm-link")
def confirm_parent_link(confirm: bool, current_student: dict = Depends(get_current_student), db: Session = Depends(get_db)):
    """Confirm or reject parent link invitation"""
    student_repo = StudentRepositoryImpl(db)
    use_case = ConfirmLinkUseCase(student_repo=student_repo)
    
    try:
        student_id = UUID(current_student['id'])
        confirmed = use_case.execute(student_id, confirm)
        return {"status": "confirmed" if confirmed else "rejected", "student_id": str(student_id)}
    except UserNotFoundException as e:
        logger.warning(f"Student not found for link confirmation: {str(e)}")
        raise HTTPException(status_code=404, detail="Student not found")
    except DomainException as e:
        logger.error(f"Link confirmation failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Link confirmation failed")

@router.get("/wallet", response_model=WalletResponse)
def get_student_wallet(current_student: dict = Depends(get_current_student), db: Session = Depends(get_db)):
    """Get student's wallet balance"""
    wallet_repo = WalletRepositoryImpl(db)
    
    try:
        student_id = UUID(current_student['id'])
        wallet = wallet_repo.get_by_student_id(student_id)
        
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found for this student")
        
        return WalletResponse(
            balance=wallet.balance,
            payer_id=wallet.student_id,
            payer_type="student"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid student ID")
