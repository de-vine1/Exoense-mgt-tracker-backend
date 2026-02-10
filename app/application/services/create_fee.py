from decimal import Decimal
from uuid import uuid4, UUID
from app.domain.entities.fee import Fee
from app.domain.repositories.fee_repository import FeeRepository

class CreateFeeUseCase:
    def __init__(self, fee_repo: FeeRepository):
        self.fee_repo = fee_repo

    def execute(self, name: str, amount: Decimal, category_id: UUID) -> Fee:
        fee = Fee(
            id=uuid4(),
            name=name,
            amount=amount,
            category_id=category_id
        )
        return self.fee_repo.save(fee)
