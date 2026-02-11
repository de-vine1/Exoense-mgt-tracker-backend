from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import Optional
from app.domain.enums.transaction_type import PayerType

class WalletBase(BaseModel):
    balance: Decimal

class WalletResponse(WalletBase):
    id: UUID
    student_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class WalletFund(BaseModel):
    amount: Decimal
    payer_id: UUID
    payer_type: PayerType
