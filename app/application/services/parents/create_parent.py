from app.application.dto.parent_dto import ParentCreate, ParentRead
from app.domain.repositories.parent_repository import ParentRepository
from app.core.security import get_password_hash

def create_parent_service(repo: ParentRepository, parent_data: ParentCreate) -> Parent:
    """
    Service to create a new parent record.
    """
    # Create the Parent entity instance
    new_parent = Parent(
        first_name=parent_data.first_name,
        last_name=parent_data.last_name,
        email=parent_data.email,
        phone_number=parent_data.phone_number,
        date_of_birth=parent_data.date_of_birth,
        gender=parent_data.gender,
        occupation=parent_data.occupation,
        hashed_password=get_password_hash(parent_data.password),
        address=parent_data.address.model_dump() if parent_data.address else None
    )
    
    # Save using the repository
    return repo.save(new_parent)
