from uuid import UUID
from app.domain.repositories.admin_repository import AdminRepository
from app.domain.exceptions import DomainException

class DeleteAdminUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self, admin_id: UUID) -> bool:
        if not self.admin_repo.delete(admin_id):
            raise DomainException(f"Admin with ID {admin_id} not found or could not be deleted")
        return True
