from uuid import UUID
from app.domain.repositories.student_repository import StudentRepository
from app.domain.exceptions import UserNotFoundException

class ConfirmLinkUseCase:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def execute(self, student_id: UUID, confirm: bool) -> bool:
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise UserNotFoundException(str(student_id))
        
        if confirm:
            student.is_link_confirmed = True
        else:
            # Reject: clear the pending parent link
            student.parent_id = None
            student.is_link_confirmed = False
            
        self.student_repo.save(student)
        return confirm
