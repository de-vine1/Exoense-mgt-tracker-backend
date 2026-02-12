from app.application.dto.staff_dto import StaffCreate
from app.domain.repositories.staff_repository import StaffRepository
from app.core.security import get_password_hash

def create_staff_service(repo: StaffRepository, staff_data: StaffCreate) -> Staff:
    """
    Service to create a new staff record.
    """
    new_staff = Staff(
        first_name=staff_data.first_name,
        last_name=staff_data.last_name,
        email=staff_data.email,
        phone_number=staff_data.phone_number,
        date_of_birth=staff_data.date_of_birth,
        gender=staff_data.gender,
        role_id=staff_data.role_id,
        department=staff_data.department,
        hashed_password=get_password_hash(staff_data.password),
        address=staff_data.address.model_dump() if staff_data.address else None
    )
    
    return repo.save(new_staff)
