from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_admin, get_staff_repo
from app.application.dto.staff_dto import StaffCreate, StaffUpdate, StaffRead
from app.application.services.staff.create_staff import create_staff_service
from app.application.services.staff.update_staff import update_staff_service
from app.application.services.staff.delete_staff import delete_staff_service
from app.application.services.staff.get_staff import (
    get_staff_by_id_service,
    get_all_staff_service,
    get_staff_by_email_service
)
from app.domain.repositories.staff_repository import StaffRepository

router = APIRouter()

@router.post("/", response_model=StaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    *,
    repo: StaffRepository = Depends(get_staff_repo),
    staff_in: StaffCreate,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Create new staff member.
    """
    staff = get_staff_by_email_service(repo, email=staff_in.email)
    if staff:
        raise HTTPException(
            status_code=400,
            detail="Staff with this email already exists.",
        )
    return create_staff_service(repo, staff_in)

@router.get("/", response_model=List[StaffRead])
def read_staff_members(
    repo: StaffRepository = Depends(get_staff_repo),
    skip: int = 0,
    limit: int = 100,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Retrieve staff members.
    """
    return get_all_staff_service(repo, skip=skip, limit=limit)

@router.get("/{staff_id}", response_model=StaffRead)
def read_staff_by_id(
    staff_id: UUID,
    repo: StaffRepository = Depends(get_staff_repo)
) -> Any:
    """
    Get staff by ID.
    """
    staff = get_staff_by_id_service(repo, staff_id=staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@router.put("/{staff_id}", response_model=StaffRead)
def update_staff(
    *,
    repo: StaffRepository = Depends(get_staff_repo),
    staff_id: UUID,
    staff_in: StaffUpdate,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Update a staff member.
    """
    staff = update_staff_service(repo, staff_id=staff_id, update_data=staff_in)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff

@router.delete("/{staff_id}", response_model=bool)
def delete_staff(
    *,
    repo: StaffRepository = Depends(get_staff_repo),
    staff_id: UUID,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Delete a staff member.
    """
    success = delete_staff_service(repo, staff_id=staff_id)
    if not success:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return success
