from typing import List
from uuid import UUID
from app.domain.repositories.student_repository import StudentRepository
from app.application.dto.student_dto import StudentResponse
from app.domain.exceptions import DomainException

class GetStudentsUseCase:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def execute(self) -> List[StudentResponse]:
        students = self.student_repo.get_all()
        return [StudentResponse.model_validate(student) for student in students]

class GetStudentByIdUseCase:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def execute(self, student_id: UUID) -> StudentResponse:
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise DomainException(f"Student with ID {student_id} not found")
        return StudentResponse.model_validate(student)
