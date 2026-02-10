from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from app.domain.entities.student_fee import StudentFee

class StudentFeeRepository(ABC):
    @abstractmethod
    def get_by_id(self, student_fee_id: UUID) -> Optional[StudentFee]:
        pass
    
    @abstractmethod
    def get_by_student_id(self, student_id: UUID) -> List[StudentFee]:
        pass
    
    @abstractmethod
    def save(self, student_fee: StudentFee) -> StudentFee:
        pass
