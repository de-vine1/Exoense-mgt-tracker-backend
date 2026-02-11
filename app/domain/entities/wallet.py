from typing import Optional
from uuid import UUID
from sqlmodel import Field
from app.domain.entities.base import BaseEntity
from app.domain.enums.wallet_type import WalletStatus
from app.domain.enums.transaction_type import Currency

class Wallet(BaseEntity, table=True):
    code: str = Field(unique=True, index=True)
    balance: str # Encrypted balance
    student_id: UUID = Field(foreign_key="student.id")
    currency: Currency = Field(default=Currency.NGN)
    status: WalletStatus = Field(default=WalletStatus.ACTIVE)