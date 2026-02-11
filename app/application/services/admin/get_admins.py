from typing import List, Optional
from uuid import UUID
from app.domain.repositories.admin_repository import AdminRepository
from app.application.dto.admin_dto import AdminResponse
from app.domain.exceptions import DomainException

class GetAdminsUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self) -> List[AdminResponse]:
        admins = self.admin_repo.get_all()
        return [AdminResponse.model_validate(admin) for admin in admins]

class GetAdminByIdUseCase:
    def __init__(self, admin_repo: AdminRepository):
        self.admin_repo = admin_repo

    def execute(self, admin_id: UUID) -> AdminResponse:
        admin = self.admin_repo.get_by_id(admin_id)
        if not admin:
            raise DomainException(f"Admin with ID {admin_id} not found")
        return AdminResponse.model_validate(admin)
