from datetime import timedelta
from app.domain.repositories.student_repository import StudentRepository
from app.domain.repositories.parent_repository import ParentRepository
from app.domain.repositories.admin_repository import AdminRepository
from app.core.security import verify_password, create_access_token
from app.application.dto.auth_dto import TokenResponse
from app.domain.exceptions import DomainException

class LoginUseCase:
    def __init__(
        self, 
        student_repo: StudentRepository,
        parent_repo: ParentRepository,
        admin_repo: AdminRepository
    ):
        self.student_repo = student_repo
        self.parent_repo = parent_repo
        self.admin_repo = admin_repo

    def execute_student(self, reg_number: str, password: str) -> TokenResponse:
        student = self.student_repo.get_by_reg_number(reg_number)
        if not student or not verify_password(password, student.hashed_password):
            raise DomainException("Invalid registration number or password")
        
        access_token = create_access_token(
            subject=student.id,
            expires_delta=timedelta(hours=1),
            # In a real app, you'd add the role to the token payload
        )
        return TokenResponse(access_token=access_token, role="student")

    def execute_parent(self, email: str, password: str) -> TokenResponse:
        parent = self.parent_repo.get_by_email(email)
        if not parent or not verify_password(password, parent.hashed_password):
            raise DomainException("Invalid email or password")
        
        access_token = create_access_token(
            subject=parent.id,
            expires_delta=timedelta(hours=1)
        )
        return TokenResponse(access_token=access_token, role="parent")

    def execute_admin(self, username_or_email: str, password: str) -> TokenResponse:
        admin = self.admin_repo.get_by_email(username_or_email) or \
                self.admin_repo.get_by_username(username_or_email)
        
        if not admin or not verify_password(password, admin.hashed_password):
            raise DomainException("Invalid credentials")
        
        access_token = create_access_token(
            subject=admin.id,
            expires_delta=timedelta(hours=1)
        )
        return TokenResponse(access_token=access_token, role="admin")
