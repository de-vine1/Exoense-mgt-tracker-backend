from uuid import UUID
from typing import Optional
from app.domain.entities.staff import Staff
from app.application.dto.staff_dto import StaffUpdate
from app.domain.repositories.staff_repository import StaffRepository

def update_staff_service(repo: StaffRepository, staff_id: UUID, update_data: StaffUpdate) -> Optional[Staff]:
    """
    Update an existing staff member's information.
    """
    staff = repo.get_by_id(staff_id)
    if not staff:
        return None
    
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        if key == 'address' and value:
            staff.address = value
        else:
            setattr(staff, key, value)
            
    return repo.save(staff)
