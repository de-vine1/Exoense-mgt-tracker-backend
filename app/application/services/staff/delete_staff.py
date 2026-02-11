from uuid import UUID
from app.domain.repositories.staff_repository import StaffRepository

def delete_staff_service(repo: StaffRepository, staff_id: UUID) -> bool:
    """
    Delete a staff record.
    """
    return repo.delete(staff_id)
