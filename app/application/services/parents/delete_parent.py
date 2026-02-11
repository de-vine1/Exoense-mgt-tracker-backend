from uuid import UUID
from app.domain.repositories.parent_repository import ParentRepository

def delete_parent_service(repo: ParentRepository, parent_id: UUID) -> bool:
    """
    Delete a parent record.
    """
    return repo.delete(parent_id)
