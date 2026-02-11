from uuid import UUID, uuid4
from app.domain.entities.admin import Admin
from app.domain.repositories.admin_repository import AdminRepository
from app.application.dto.admin_dto import AdminCreate, AdminResponse
from app.core.security import get_password_hash
from app.domain.exceptions import DomainException

class RegisterAdminUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self, admin_in: AdminCreate) -> AdminResponse:
        # Check if username already exists
        if self.admin_repo.get_by_username(admin_in.username):
            raise DomainException(f"Username {admin_in.username} already exists")
        
        # Check if email already exists
        if self.admin_repo.get_by_email(admin_in.email):
            raise DomainException(f"Email {admin_in.email} already exists")
        
        admin = Admin(
            id=uuid4(),
            firstname=admin_in.firstname,
            lastname=admin_in.lastname,
            username=admin_in.username,
            email=admin_in.email,
            hashed_password=get_password_hash(admin_in.password),
        )
        
        saved_admin = self.admin_repo.save(admin)
        return AdminResponse.model_validate(saved_admin)
