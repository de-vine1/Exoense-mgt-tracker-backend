from decimal import Decimal
from uuid import UUID, uuid4
from app.domain.repositories.wallet_repository import WalletRepository
from app.domain.repositories.transaction_repository import TransactionRepository
from app.domain.entities.transaction import Transaction
from app.domain.enums.transaction_type import TransactionStatus, PaymentMethod, Gateway, PayerType
from app.domain.exceptions import WalletNotFoundException

class FundWalletUseCase:
    def __init__(
        self, 
        wallet_repo: WalletRepository, 
        transaction_repo: TransactionRepository
    ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    def execute(self, payer_id: UUID, payer_type: PayerType, amount: Decimal) -> bool:
        wallet = None
        if payer_type == PayerType.STUDENT:
            wallet = self.wallet_repo.get_by_student_id(payer_id)
        else:
            wallet = self.wallet_repo.get_by_parent_id(payer_id)
            
        if not wallet:
            raise WalletNotFoundException(str(payer_id))
        
        # In a real app, you'd verify with the payment gateway here
        # For now, we'll assume success and update balance
        wallet.balance += amount
        self.wallet_repo.save(wallet)
        
        # Log transaction
        transaction = Transaction(
            id=uuid4(),
            amount=amount,
            status=TransactionStatus.SUCCESS,
            payer_id=payer_id,
            payer_type=payer_type,
            description=f"Wallet Top-up via {payer_type.value}",
            gateway=Gateway.FLUTTERWAVE, # Default
            payment_method=PaymentMethod.CARD
        )
        self.transaction_repo.save(transaction)
        
        return True
