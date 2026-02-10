from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.student import Student

class StudentRepository(ABC):
    @abstractmethod
    def get_by_id(self, student_id: UUID) -> Optional[Student]:
        pass
    
    @abstractmethod
    def get_by_reg_number(self, reg_number: str) -> Optional[Student]:
        pass
    
    @abstractmethod
    def save(self, student: Student) -> Student:
        pass
    
    @abstractmethod
    def get_pending_links(self, student_id: UUID) -> List[Student]:
        pass
