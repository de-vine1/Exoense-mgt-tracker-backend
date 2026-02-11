from uuid import UUID
from typing import Optional, List
from app.domain.entities.staff import Staff
from app.domain.repositories.staff_repository import StaffRepository

def get_staff_by_id_service(repo: StaffRepository, staff_id: UUID) -> Optional[Staff]:
    """Retrieve a staff member by their ID."""
    return repo.get_by_id(staff_id)

def get_all_staff_service(repo: StaffRepository, skip: int = 0, limit: int = 100) -> List[Staff]:
    """Retrieve a list of all staff members."""
    return repo.get_all(skip=skip, limit=limit)

def get_staff_by_email_service(repo: StaffRepository, email: str) -> Optional[Staff]:
    """Retrieve a staff member by their email."""
    return repo.get_by_email(email)
