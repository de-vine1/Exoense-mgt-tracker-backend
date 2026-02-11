from uuid import UUID
from app.domain.repositories.student_repository import StudentRepository
from app.domain.exceptions import DomainException

class DeleteStudentUseCase:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def execute(self, student_id: UUID) -> bool:
        if not self.student_repo.delete(student_id):
            raise DomainException(f"Student with ID {student_id} not found or could not be deleted")
        return True
