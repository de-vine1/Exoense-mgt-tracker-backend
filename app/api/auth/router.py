from fastapi import APIRouter
from .schemas import LoginRequest, TokenResponse
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    # fake validation for now
    token = create_access_token(subject=data.email, role="admin")
    return {"access_token": token}
