from typing import List, Optional
from uuid import UUID
from app.domain.repositories.wallet_repository import WalletRepository
from app.domain.entities.wallet import Wallet
from app.domain.enums.transaction_type import PayerType
from app.domain.exceptions import WalletNotFoundException

class GetWalletsUseCase:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    def execute(self) -> List[Wallet]:
        return self.wallet_repo.get_all()

class GetWalletByOwnerUseCase:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    def execute(self, owner_id: UUID, owner_type: PayerType) -> Wallet:
        wallet = None
        if owner_type == PayerType.STUDENT:
            wallet = self.wallet_repo.get_by_student_id(owner_id)
        else:
            wallet = self.wallet_repo.get_by_parent_id(owner_id)
            
        if not wallet:
            raise WalletNotFoundException(str(owner_id))
        return wallet
