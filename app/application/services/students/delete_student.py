from uuid import UUID
from app.domain.repositories.student_repository import StudentRepository

def delete_student_service(repo: StudentRepository, student_id: UUID) -> bool:
    """
    Delete a student record.
    """
    return repo.delete(student_id)
