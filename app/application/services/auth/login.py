from typing import Optional, Any
from app.core.security import verify_password, create_access_token
from app.domain.repositories.student_repository import StudentRepository
from app.domain.repositories.parent_repository import ParentRepository
from app.domain.repositories.staff_repository import StaffRepository

def authenticate_user(repo: Any, email: str, password: str) -> Optional[Any]:
    """
    Find user by email and verify password.
    Generic for any repository that provides get_by_email.
    """
    user = repo.get_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def login_student_service(repo: StudentRepository, email: str, password: str) -> Optional[dict]:
    """
    Handles student login and returns tokens.
    """
    user = authenticate_user(repo, email, password)
    if not user:
        return None
    
    access_token = create_access_token(subject=user.id, role="student")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": "student",
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }

def login_parent_service(repo: ParentRepository, email: str, password: str) -> Optional[dict]:
    """
    Handles parent login and returns tokens.
    """
    user = authenticate_user(repo, email, password)
    if not user:
        return None
    
    access_token = create_access_token(subject=user.id, role="parent")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": "parent",
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }

def login_staff_service(repo: StaffRepository, email: str, password: str) -> Optional[dict]:
    """
    Handles staff login and returns tokens.
    """
    user = authenticate_user(repo, email, password)
    if not user:
        return None
    
    # Staff role might need more granularity later (e.g., admin vs staff)
    # For now, following the role field in JWT
    role = "staff"
    # Logic to check if user.role_id suggests an admin can go here if needed
    
    access_token = create_access_token(subject=user.id, role=role)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": role,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }
