from uuid import UUID
from app.domain.repositories.parent_repository import ParentRepository
from app.application.dto.parent_dto import ParentUpdate, ParentResponse
from app.core.security import get_password_hash
from app.domain.exceptions import DomainException

class UpdateParentUseCase:
    def __init__(self, parent_repo: ParentRepository):
        self.parent_repo = parent_repo

    def execute(self, parent_id: UUID, parent_in: ParentUpdate) -> ParentResponse:
        parent = self.parent_repo.get_by_id(parent_id)
        if not parent:
            raise DomainException(f"Parent with ID {parent_id} not found")

        update_data = parent_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        if "email" in update_data and update_data["email"] != parent.email:
            if self.parent_repo.get_by_email(update_data["email"]):
                raise DomainException(f"Email {update_data['email']} already exists")

        for key, value in update_data.items():
            setattr(parent, key, value)
        
        saved_parent = self.parent_repo.save(parent)
        return ParentResponse.model_validate(saved_parent)
