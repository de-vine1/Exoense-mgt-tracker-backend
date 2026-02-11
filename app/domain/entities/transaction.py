from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlmodel import Field
from app.domain.entities.base import BaseEntity
from app.domain.enums.transaction_type import TransactionStatus

class WalletTransaction(BaseEntity, table=True):
    wallet_id: UUID = Field(foreign_key="wallet.id")
    amount: float
    transaction_id: str = Field(unique=True, index=True)
    external_transaction_id: Optional[str] = None
    transaction_date: datetime = Field(default_factory=datetime.now)
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)