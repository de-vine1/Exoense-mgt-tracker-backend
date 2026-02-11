from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from app.application.dto.base_dto import BaseDTO
from app.domain.enums.transaction_type import TransactionStatus

class WalletTransactionRead(BaseDTO):
    wallet_id: UUID
    amount: float
    transaction_id: str
    external_transaction_id: Optional[str] = None
    transaction_date: datetime
    status: TransactionStatus
