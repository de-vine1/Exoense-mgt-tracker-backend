from uuid import UUID
from typing import Optional
from app.domain.entities.parent import Parent
from app.application.dto.parent_dto import ParentUpdate
from app.domain.repositories.parent_repository import ParentRepository

def update_parent_service(repo: ParentRepository, parent_id: UUID, update_data: ParentUpdate) -> Optional[Parent]:
    """
    Update an existing parent's information.
    """
    # Retrieve the existing parent
    parent = repo.get_by_id(parent_id)
    if not parent:
        return None
    
    # Update fields if provided
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        if key == 'address' and value:
            # Handle nested address update
            parent.address = value # Already a dict from model_dump
        else:
            setattr(parent, key, value)
            
    # Save the updated entity
    return repo.save(parent)
