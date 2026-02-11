from uuid import UUID
from app.domain.repositories.admin_repository import AdminRepository
from app.application.dto.admin_dto import AdminUpdate, AdminResponse
from app.core.security import get_password_hash
from app.domain.exceptions import DomainException

class UpdateAdminUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self, admin_id: UUID, admin_in: AdminUpdate) -> AdminResponse:
        admin = self.admin_repo.get_by_id(admin_id)
        if not admin:
            raise DomainException(f"Admin with ID {admin_id} not found")

        update_data = admin_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        # Check for uniqueness if username or email is being updated
        if "username" in update_data and update_data["username"] != admin.username:
            if self.admin_repo.get_by_username(update_data["username"]):
                raise DomainException(f"Username {update_data['username']} already exists")
        
        if "email" in update_data and update_data["email"] != admin.email:
            if self.admin_repo.get_by_email(update_data["email"]):
                raise DomainException(f"Email {update_data['email']} already exists")

        for key, value in update_data.items():
            setattr(admin, key, value)
        
        saved_admin = self.admin_repo.save(admin)
        return AdminResponse.model_validate(saved_admin)
