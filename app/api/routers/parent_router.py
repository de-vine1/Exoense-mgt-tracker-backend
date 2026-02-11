from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_parent_repo, get_current_admin
from app.application.dto.parent_dto import ParentCreate, ParentUpdate, ParentRead
from app.application.services.parents.create_parent import create_parent_service
from app.application.services.parents.update_parent import update_parent_service
from app.application.services.parents.delete_parent import delete_parent_service
from app.application.services.parents.get_parent import (
    get_parent_by_id_service, 
    get_all_parents_service,
    get_parent_by_email_service
)
from app.domain.repositories.parent_repository import ParentRepository

router = APIRouter()

@router.post("/", response_model=ParentRead, status_code=status.HTTP_201_CREATED)
def create_parent(
    *,
    repo: ParentRepository = Depends(get_parent_repo),
    parent_in: ParentCreate
) -> Any:
    """
    Create new parent.
    """
    parent = get_parent_by_email_service(repo, email=parent_in.email)
    if parent:
        raise HTTPException(
            status_code=400,
            detail="A parent with this email already exists in the system.",
        )
    return create_parent_service(repo, parent_in)

@router.get("/", response_model=List[ParentRead])
def read_parents(
    repo: ParentRepository = Depends(get_parent_repo),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve parents.
    """
    return get_all_parents_service(repo, skip=skip, limit=limit)

@router.get("/{parent_id}", response_model=ParentRead)
def read_parent_by_id(
    parent_id: UUID,
    repo: ParentRepository = Depends(get_parent_repo)
) -> Any:
    """
    Get parent by ID.
    """
    parent = get_parent_by_id_service(repo, parent_id=parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.put("/{parent_id}", response_model=ParentRead)
def update_parent(
    *,
    repo: ParentRepository = Depends(get_parent_repo),
    parent_id: UUID,
    parent_in: ParentUpdate
) -> Any:
    """
    Update a parent.
    """
    parent = update_parent_service(repo, parent_id=parent_id, update_data=parent_in)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.delete("/{parent_id}", response_model=bool)
def delete_parent(
    *,
    repo: ParentRepository = Depends(get_parent_repo),
    parent_id: UUID,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Delete a parent.
    """
    success = delete_parent_service(repo, parent_id=parent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Parent not found")
    return success
