from fastapi import APIRouter, Depends, HTTPException
from app.application.dto.auth_dto import LoginRequest, TokenResponse
from app.application.services.login_use_case import LoginUseCase
from app.domain.exceptions import DomainException

router = APIRouter(prefix="/auth", tags=["auth"])

# Note: In a real implementation with DI, you'd inject the LoginUseCase here.
# For this structure, we'll assume a way to get the use case instance.

@router.post("/login/student", response_model=TokenResponse)
def login_student(request: LoginRequest):
    # This is a placeholder for the actual service call
    # In a full Clean Arch, you'd use a dependency to get the LoginUseCase
    return {"access_token": "token", "token_type": "bearer", "role": "student"}

@router.post("/login/parent", response_model=TokenResponse)
def login_parent(request: LoginRequest):
    return {"access_token": "token", "token_type": "bearer", "role": "parent"}

@router.post("/login/admin", response_model=TokenResponse)
def login_admin(request: LoginRequest):
    return {"access_token": "token", "token_type": "bearer", "role": "admin"}
