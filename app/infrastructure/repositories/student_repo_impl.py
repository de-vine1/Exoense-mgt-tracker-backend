from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository


class StudentRepositoryImpl(StudentRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, student_id: UUID) -> Optional[Student]:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_by_reg_number(self, reg_number: str) -> Optional[Student]:
        return self.db.query(Student).filter(Student.reg_number == reg_number).first()

    def get_by_email(self, email: str) -> Optional[Student]:
        return self.db.query(Student).filter(Student.email == email).first()

    def save(self, student: Student) -> Student:
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_all(self) -> List[Student]:
        return self.db.query(Student).all()

    def get_pending_links(self, student_id: UUID) -> List[Student]:
        return self.db.query(Student).filter(
            Student.parent_id == student_id,
            Student.is_link_confirmed == False
        ).all()

    def get_by_parent_id(self, parent_id: UUID) -> List[Student]:
        return self.db.query(Student).filter(Student.parent_id == parent_id).all()

    def delete(self, student_id: UUID) -> bool:
        student = self.get_by_id(student_id)
        if student:
            self.db.delete(student)
            self.db.commit()
            return True
        return False

