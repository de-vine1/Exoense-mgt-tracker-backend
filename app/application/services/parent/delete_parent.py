from uuid import UUID
from app.domain.repositories.parent_repository import ParentRepository
from app.domain.exceptions import DomainException

class DeleteParentUseCase:
    def __init__(self, parent_repo: ParentRepository):
        self.parent_repo = parent_repo

    def execute(self, parent_id: UUID) -> bool:
        if not self.parent_repo.delete(parent_id):
            raise DomainException(f"Parent with ID {parent_id} not found or could not be deleted")
        return True
