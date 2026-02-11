from uuid import UUID
from typing import Optional
from app.domain.entities.student import Student
from app.application.dto.student_dto import StudentUpdate
from app.domain.repositories.student_repository import StudentRepository

def update_student_service(repo: StudentRepository, student_id: UUID, update_data: StudentUpdate) -> Optional[Student]:
    """
    Update an existing student's information.
    """
    student = repo.get_by_id(student_id)
    if not student:
        return None
    
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        if key == 'address' and value:
            student.address = value
        else:
            setattr(student, key, value)
            
    return repo.save(student)
