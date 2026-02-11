from uuid import UUID
from app.domain.entities.wallet import Wallet
from app.application.dto.wallet_dto import WalletCreate
from app.domain.repositories.wallet_repository import WalletRepository
from app.domain.enums.wallet_type import WalletStatus
from app.domain.enums.transaction_type import Currency

def create_wallet_service(repo: WalletRepository, student_id: UUID, code: str) -> Wallet:
    """
    Initialize a new wallet for a student.
    Initially starting with a balance of "0.0" (encrypted string).
    """
    # Check if student already has a wallet
    existing_wallet = repo.get_by_student_id(student_id)
    if existing_wallet:
        return existing_wallet
    
    new_wallet = Wallet(
        code=code,
        balance="0.0", # Placeholder for encrypted balance
        student_id=student_id,
        currency=Currency.NGN,
        status=WalletStatus.ACTIVE
    )
    
    return repo.save(new_wallet)
