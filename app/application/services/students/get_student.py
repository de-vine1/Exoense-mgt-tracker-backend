from uuid import UUID
from typing import Optional, List
from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository

def get_student_by_id_service(repo: StudentRepository, student_id: UUID) -> Optional[Student]:
    """Retrieve a student by their ID."""
    return repo.get_by_id(student_id)

def get_all_students_service(repo: StudentRepository, skip: int = 0, limit: int = 100) -> List[Student]:
    """Retrieve a list of all students."""
    return repo.get_all(skip=skip, limit=limit)

def get_student_by_reg_number_service(repo: StudentRepository, reg_number: str) -> Optional[Student]:
    """Retrieve a student by their registration number."""
    return repo.get_by_reg_number(reg_number)

def get_student_by_email_service(repo: StudentRepository, email: str) -> Optional[Student]:
    """Retrieve a student by their email."""
    return repo.get_by_email(email)
