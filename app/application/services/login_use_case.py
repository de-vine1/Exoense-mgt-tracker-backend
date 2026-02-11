from datetime import timedelta
from typing import Optional
from app.domain.repositories.student_repository import StudentRepository
from app.domain.repositories.parent_repository import ParentRepository
from app.domain.repositories.admin_repository import AdminRepository
from app.core.security import verify_password, create_access_token
from app.application.dto.auth_dto import TokenResponse
from app.domain.exceptions import DomainException

class LoginUseCase:
    def __init__(
        self, 
        student_repo: Optional[StudentRepository] = None,
        parent_repo: Optional[ParentRepository] = None,
        admin_repo: Optional[AdminRepository] = None
    ):
        self.student_repo = student_repo
        self.parent_repo = parent_repo
        self.admin_repo = admin_repo

    def execute_student(self, reg_number: str, password: str) -> TokenResponse:
        student = self.student_repo.get_by_reg_number(reg_number)
        if not student or not verify_password(password, student.hashed_password):
            raise DomainException("Invalid Credentials")
        
        access_token = create_access_token(
            subject=student.id,
            role="student",
            expires_delta=timedelta(hours=1)
        )
        return TokenResponse(access_token=access_token, role="student")

    def execute_parent(self, email: str, password: str) -> TokenResponse:
        parent = self.parent_repo.get_by_email(email)
        if not parent or not verify_password(password, parent.hashed_password):
            raise DomainException("Invalid Credentials")
        
        access_token = create_access_token(
            subject=parent.id,
            role="parent",
            expires_delta=timedelta(hours=1)
        )
        return TokenResponse(access_token=access_token, role="parent")

    def execute_admin(self, username_or_email: str, password: str) -> TokenResponse:
        admin = self.admin_repo.get_by_email(username_or_email) or \
                self.admin_repo.get_by_username(username_or_email)
        
        if not admin or not verify_password(password, admin.hashed_password):
            raise DomainException("Invalid Credentials")
        
        access_token = create_access_token(
            subject=admin.id,
            role="admin",
            expires_delta=timedelta(hours=1)
        )
        return TokenResponse(access_token=access_token, role="admin")
