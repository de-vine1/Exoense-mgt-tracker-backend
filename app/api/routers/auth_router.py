from fastapi import APIRouter, Depends, HTTPException, status
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

# --- Dependency Providers ---

def get_student_login_use_case(db: Session = Depends(get_db)) -> LoginUseCase:
    return LoginUseCase(student_repo=StudentRepositoryImpl(db))

def get_parent_login_use_case(db: Session = Depends(get_db)) -> LoginUseCase:
    return LoginUseCase(parent_repo=ParentRepositoryImpl(db))

def get_admin_login_use_case(db: Session = Depends(get_db)) -> LoginUseCase:
    return LoginUseCase(admin_repo=AdminRepositoryImpl(db))

# --- Routes ---

@router.post("/login/student", response_model=TokenResponse)
def login_student(
    login_request: LoginRequest, 
    use_case: LoginUseCase = Depends(get_student_login_use_case)
):
    """Authenticate student using registration number and password"""
    try:
        return use_case.execute_student(login_request.username_or_email_or_reg, login_request.password)
    except DomainException as e:
        logger.warning(f"Student login failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

@router.post("/login/parent", response_model=TokenResponse)
def login_parent(
    login_request: LoginRequest, 
    use_case: LoginUseCase = Depends(get_parent_login_use_case)
):
    """Authenticate parent using email and password"""
    try:
        return use_case.execute_parent(login_request.username_or_email_or_reg, login_request.password)
    except DomainException as e:
        logger.warning(f"Parent login failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

@router.post("/login/admin", response_model=TokenResponse)
def login_admin(
    login_request: LoginRequest, 
    use_case: LoginUseCase = Depends(get_admin_login_use_case)
):
    """Authenticate admin using username/email and password"""
    try:
        return use_case.execute_admin(login_request.username_or_email_or_reg, login_request.password)
    except DomainException as e:
        logger.warning(f"Admin login failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")


