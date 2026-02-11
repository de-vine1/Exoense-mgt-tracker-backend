from uuid import UUID
from app.domain.repositories.student_repository import StudentRepository
from app.application.dto.student_dto import StudentUpdate, StudentResponse
from app.core.security import get_password_hash
from app.domain.exceptions import DomainException

class UpdateStudentUseCase:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def execute(self, student_id: UUID, student_in: StudentUpdate) -> StudentResponse:
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise DomainException(f"Student with ID {student_id} not found")

        update_data = student_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        if "email" in update_data and update_data["email"] != student.email:
            if self.student_repo.get_by_email(update_data["email"]):
                raise DomainException(f"Email {update_data['email']} already exists")


        for key, value in update_data.items():
            setattr(student, key, value)
        
        saved_student = self.student_repo.save(student)
        return StudentResponse.model_validate(saved_student)
