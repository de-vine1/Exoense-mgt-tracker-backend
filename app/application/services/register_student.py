from uuid import UUID, uuid4
from app.domain.entities.student import Student
from app.domain.entities.wallet import Wallet
from app.domain.repositories.student_repository import StudentRepository
from app.domain.repositories.wallet_repository import WalletRepository
from app.application.dto.student_dto import StudentCreate, StudentResponse
from app.core.security import get_password_hash

class RegisterStudentUseCase:
    def __init__(
        self, 
        student_repo: StudentRepository, 
        wallet_repo: WalletRepository
    ):
        self.student_repo = student_repo
        self.wallet_repo = wallet_repo

    def execute(self, student_in: StudentCreate) -> StudentResponse:
        student = Student(
            id=uuid4(),
            reg_number=student_in.reg_number,
            firstname=student_in.firstname,
            lastname=student_in.lastname,
            email=student_in.email,
            grade=student_in.grade,
            term=student_in.term,
            hashed_password=get_password_hash(student_in.password),
        )
        saved_student = self.student_repo.save(student)
        
        # Automatically create wallet for student
        wallet = Wallet(
            id=uuid4(),
            student_id=saved_student.id,
            balance=0.0
        )
        self.wallet_repo.save(wallet)
        
        return StudentResponse.from_orm(saved_student)
