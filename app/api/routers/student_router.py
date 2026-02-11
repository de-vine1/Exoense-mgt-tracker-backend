from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_student_repo, get_current_admin
from app.application.dto.student_dto import StudentCreate, StudentUpdate, StudentRead
from app.application.services.students.create_student import create_student_service
from app.application.services.students.update_student import update_student_service
from app.application.services.students.delete_student import delete_student_service
from app.application.services.students.get_student import (
    get_student_by_id_service,
    get_all_students_service,
    get_student_by_reg_number_service
)
from app.domain.repositories.student_repository import StudentRepository

router = APIRouter()

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    *,
    repo: StudentRepository = Depends(get_student_repo),
    student_in: StudentCreate
) -> Any:
    """
    Create new student.
    """
    student = get_student_by_reg_number_service(repo, reg_number=student_in.reg_number)
    if student:
        raise HTTPException(
            status_code=400,
            detail="A student with this registration number already exists.",
        )
    return create_student_service(repo, student_in)

@router.get("/", response_model=List[StudentRead])
def read_students(
    repo: StudentRepository = Depends(get_student_repo),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve students.
    """
    return get_all_students_service(repo, skip=skip, limit=limit)

@router.get("/{student_id}", response_model=StudentRead)
def read_student_by_id(
    student_id: UUID,
    repo: StudentRepository = Depends(get_student_repo)
) -> Any:
    """
    Get student by ID.
    """
    student = get_student_by_id_service(repo, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=StudentRead)
def update_student(
    *,
    repo: StudentRepository = Depends(get_student_repo),
    student_id: UUID,
    student_in: StudentUpdate
) -> Any:
    """
    Update a student.
    """
    student = update_student_service(repo, student_id=student_id, update_data=student_in)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}", response_model=bool)
def delete_student(
    *,
    repo: StudentRepository = Depends(get_student_repo),
    student_id: UUID,
    current_admin: Any = Depends(get_current_admin)
) -> Any:
    """
    Delete a student.
    """
    success = delete_student_service(repo, student_id=student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return success
