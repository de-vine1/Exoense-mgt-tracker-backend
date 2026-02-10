from decimal import Decimal
from datetime import datetime
from uuid import UUID, uuid4
from app.domain.repositories.wallet_repository import WalletRepository
from app.domain.repositories.student_fee_repository import StudentFeeRepository
from app.domain.repositories.transaction_repository import TransactionRepository
from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_type import TransactionStatus, PaymentMethod, PayerType
from app.domain.exceptions import WalletNotFoundException, DomainException

class PayFeeUseCase:
    def __init__(
        self, 
        wallet_repo: WalletRepository, 
        student_fee_repo: StudentFeeRepository,
        transaction_repo: TransactionRepository
    ):
        self.wallet_repo = wallet_repo
        self.student_fee_repo = student_fee_repo
        self.transaction_repo = transaction_repo

    def execute(self, payer_id: UUID, payer_type: PayerType, student_fee_id: UUID, amount: Decimal) -> bool:
        # 1. Get the wallet of the payer
        wallet = None
        if payer_type == PayerType.STUDENT:
            wallet = self.wallet_repo.get_by_student_id(payer_id)
        else:
            wallet = self.wallet_repo.get_by_parent_id(payer_id)
            
        if not wallet:
            raise WalletNotFoundException(str(payer_id))
        
        # 2. Check balance
        if wallet.balance < amount:
            raise DomainException("Insufficient wallet balance")
            
        # 3. Get the student fee record
        student_fee = self.student_fee_repo.get_by_id(student_fee_id)
        if not student_fee:
            raise DomainException("Student fee record not found")
        
        # 4. Deduct from wallet
        wallet.balance -= amount
        self.wallet_repo.save(wallet)
        
        # 5. Update student fee paid amount
        student_fee.amount_paid += amount
        if student_fee.amount_paid >= student_fee.amount_due:
            student_fee.is_paid = True
            student_fee.paid_at = datetime.now()
        self.student_fee_repo.save(student_fee)
        
        # 6. Log transaction
        transaction = Transaction(
            id=uuid4(),
            amount=amount,
            status=TransactionStatus.SUCCESS,
            payer_id=payer_id,
            payer_type=payer_type,
            description=f"Fee Payment for student {student_fee.student_id}",
            payment_method=PaymentMethod.WALLET
        )
        self.transaction_repo.save(transaction)
        
        return True
