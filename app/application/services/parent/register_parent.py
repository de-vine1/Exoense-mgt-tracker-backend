from uuid import UUID, uuid4
from app.domain.entities.parent import Parent
from app.domain.entities.wallet import Wallet
from app.domain.repositories.parent_repository import ParentRepository
from app.domain.repositories.wallet_repository import WalletRepository
from app.application.dto.parent_dto import ParentCreate, ParentResponse
from app.core.security import get_password_hash

class RegisterParentUseCase:
    def __init__(
        self, 
        parent_repo: ParentRepository, 
        wallet_repo: WalletRepository
    ):
        self.parent_repo = parent_repo
        self.wallet_repo = wallet_repo

    def execute(self, parent_in: ParentCreate) -> ParentResponse:
        parent = Parent(
            id=uuid4(),
            firstname=parent_in.firstname,
            lastname=parent_in.lastname,
            email=parent_in.email,
            hashed_password=get_password_hash(parent_in.password),
        )
        saved_parent = self.parent_repo.save(parent)
        
        # Automatically create wallet for parent
        wallet = Wallet(
            id=uuid4(),
            parent_id=saved_parent.id,
            balance=0.0
        )
        self.wallet_repo.save(wallet)
        
        return ParentResponse.model_validate(saved_parent)
