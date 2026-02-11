from uuid import UUID
from app.domain.repositories.student_repository import StudentRepository
from app.domain.exceptions import UserNotFoundException

class InviteStudentUseCase:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def execute(self, parent_id: UUID, student_reg_number: str) -> bool:
        student = self.student_repo.get_by_reg_number(student_reg_number)
        if not student:
            raise UserNotFoundException(student_reg_number)
        
        # Link student to parent but don't confirm yet
        student.parent_id = parent_id
        student.is_link_confirmed = False
        
        self.student_repo.save(student)
        return True
