from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import logging
from app.application.dto.auth_dto import LoginRequest, TokenResponse
from app.application.services.login_use_case import LoginUseCase
from app.infrastructure.repositories.student_repo_impl import StudentRepositoryImpl
from app.infrastructure.repositories.parent_repo_impl import ParentRepositoryImpl
from app.infrastructure.repositories.admin_repo_impl import AdminRepositoryImpl
from app.infrastructure.database.session import get_db
from app.domain.exceptions import DomainException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/student", response_model=TokenResponse)
def login_student(login_request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate student using registration number and password"""
    student_repo = StudentRepositoryImpl(db)
    use_case = LoginUseCase(student_repo=student_repo)
    
    try:
        return use_case.execute_student(login_request.username_or_email_or_reg, login_request.password)
    except DomainException as e:
        logger.warning(f"Student login failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid Credentials")

@router.post("/login/parent", response_model=TokenResponse)
def login_parent(login_request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate parent using email and password"""
    parent_repo = ParentRepositoryImpl(db)
    use_case = LoginUseCase(parent_repo=parent_repo)
    
    try:
        return use_case.execute_parent(login_request.username_or_email_or_reg, login_request.password)
    except DomainException as e:
        logger.warning(f"Parent login failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid Credentials")

@router.post("/login/admin", response_model=TokenResponse)
def login_admin(login_request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate admin using username/email and password"""
    admin_repo = AdminRepositoryImpl(db)
    use_case = LoginUseCase(admin_repo=admin_repo)
    
    try:
        return use_case.execute_admin(login_request.username_or_email_or_reg, login_request.password)
    except DomainException as e:
        logger.warning(f"Admin login failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid Credentials")

