from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional
from app.domain.enums.transaction_type import TransactionStatus, PaymentMethod, Gateway, PayerType

class TransactionResponse(BaseModel):
    id: UUID
    amount: Decimal
    status: TransactionStatus
    gateway: Gateway
    payment_method: PaymentMethod
    payer_id: UUID
    payer_type: PayerType
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
