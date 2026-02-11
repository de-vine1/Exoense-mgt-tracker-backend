from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.application.dto.base_dto import BaseDTO
from app.domain.enums.wallet_type import WalletStatus
from app.domain.enums.transaction_type import Currency

class WalletBase(BaseModel):
    code: str
    student_id: UUID
    currency: Currency = Currency.NGN

class WalletCreate(WalletBase):
    balance: str # Encrypted balance initially

class WalletUpdate(BaseModel):
    balance: Optional[str] = None
    status: Optional[WalletStatus] = None
    currency: Optional[Currency] = None

class WalletRead(WalletBase, BaseDTO):
    balance: str
    status: WalletStatus
