from uuid import UUID
from typing import Optional, List
from app.domain.entities.parent import Parent
from app.domain.repositories.parent_repository import ParentRepository

def get_parent_by_id_service(repo: ParentRepository, parent_id: UUID) -> Optional[Parent]:
    """Retrieve a parent by their ID."""
    return repo.get_by_id(parent_id)

def get_all_parents_service(repo: ParentRepository, skip: int = 0, limit: int = 100) -> List[Parent]:
    """Retrieve a list of all parents."""
    return repo.get_all(skip=skip, limit=limit)

def get_parent_by_email_service(repo: ParentRepository, email: str) -> Optional[Parent]:
    """Retrieve a parent by their email."""
    return repo.get_by_email(email)
