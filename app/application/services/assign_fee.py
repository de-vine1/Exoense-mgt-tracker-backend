from uuid import uuid4, UUID
from app.domain.entities.student_fee import StudentFee
from app.domain.repositories.student_fee_repository import StudentFeeRepository
from app.domain.repositories.fee_repository import FeeRepository
from app.domain.exceptions import DomainException

class AssignFeeToStudentUseCase:
    def __init__(
        self, 
        student_fee_repo: StudentFeeRepository,
        fee_repo: FeeRepository
    ):
        self.student_fee_repo = student_fee_repo
        self.fee_repo = fee_repo

    def execute(self, student_id: UUID, fee_id: UUID) -> StudentFee:
        fee = self.fee_repo.get_by_id(fee_id)
        if not fee:
            raise DomainException("Fee not found")
            
        student_fee = StudentFee(
            id=uuid4(),
            student_id=student_id,
            fee_id=fee_id,
            amount_due=fee.amount,
            amount_paid=0.0,
            is_paid=False
        )
        return self.student_fee_repo.save(student_fee)
