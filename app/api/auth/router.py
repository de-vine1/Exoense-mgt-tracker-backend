from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import LoginRequest, TokenResponse
from app.api.deps import get_student_repo, get_parent_repo, get_staff_repo
from app.application.services.auth.login import (
    login_student_service,
    login_parent_service,
    login_staff_service
)
from app.domain.repositories.student_repository import StudentRepository
from app.domain.repositories.parent_repository import ParentRepository
from app.domain.repositories.staff_repository import StaffRepository

router = APIRouter()

@router.post("/login/student", response_model=TokenResponse)
def login_student(
    data: LoginRequest,
    repo: StudentRepository = Depends(get_student_repo)
) -> Any:
    """
    Login endpoint for students.
    """
    result = login_student_service(repo, data.email, data.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return result

@router.post("/login/parent", response_model=TokenResponse)
def login_parent(
    data: LoginRequest,
    repo: ParentRepository = Depends(get_parent_repo)
) -> Any:
    """
    Login endpoint for parents.
    """
    result = login_parent_service(repo, data.email, data.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return result

@router.post("/login/staff", response_model=TokenResponse)
def login_staff(
    data: LoginRequest,
    repo: StaffRepository = Depends(get_staff_repo)
) -> Any:
    """
    Login endpoint for staff.
    """
    result = login_staff_service(repo, data.email, data.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return result
