from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from app.domain.enums.transaction_type import TransactionStatus, PaymentMethod, Gateway, PayerType

class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    amount: Decimal = Field(decimal_places=2)
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    
    gateway: Gateway = Field(default=Gateway.FLUTTERWAVE)
    gateway_transaction_id: Optional[str] = Field(default=None, index=True)
    payment_method: PaymentMethod = Field(default=PaymentMethod.CARD)
    
    payer_id: UUID = Field(index=True) 
    payer_type: PayerType = Field()
    
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)