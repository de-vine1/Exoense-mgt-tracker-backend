from typing import List
from uuid import UUID
from app.domain.repositories.parent_repository import ParentRepository
from app.application.dto.parent_dto import ParentResponse
from app.domain.exceptions import DomainException

class GetParentsUseCase:
    def __init__(self, parent_repo: ParentRepository):
        self.parent_repo = parent_repo

    def execute(self) -> List[ParentResponse]:
        parents = self.parent_repo.get_all()
        return [ParentResponse.model_validate(parent) for parent in parents]

class GetParentByIdUseCase:
    def __init__(self, parent_repo: ParentRepository):
        self.parent_repo = parent_repo

    def execute(self, parent_id: UUID) -> ParentResponse:
        parent = self.parent_repo.get_by_id(parent_id)
        if not parent:
            raise DomainException(f"Parent with ID {parent_id} not found")
        return ParentResponse.model_validate(parent)
