from app.domain.entities.student import Student
from app.application.dto.student_dto import StudentCreate
from app.domain.repositories.student_repository import StudentRepository

def create_student_service(repo: StudentRepository, student_data: StudentCreate) -> Student:
    """
    Service to create a new student record.
    """
    new_student = Student(
        first_name=student_data.first_name,
        last_name=student_data.last_name,
        email=student_data.email,
        phone_number=student_data.phone_number,
        date_of_birth=student_data.date_of_birth,
        gender=student_data.gender,
        reg_number=student_data.reg_number,
        class_name=student_data.class_name,
        group_name=student_data.group_name,
        image=student_data.image,
        qr_code=student_data.qr_code,
        address=student_data.address.model_dump() if student_data.address else None
    )
    
    return repo.save(new_student)
