from datetime import datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel
from app.application.dto.base_dto import BaseDTO
from app.domain.enums.entity_type import EntityStatus

class SaleDetailBase(BaseModel):
    product_name: str
    product_id: UUID
    amount: float
    discount_amount: float = 0.0
    charge_amount: float = 0.0
    quantity: int = 1

class SaleDetailCreate(SaleDetailBase):
    pass

class SaleDetailRead(SaleDetailBase, BaseDTO):
    sale_id: UUID

class SaleBase(BaseModel):
    transaction_id: str
    transaction_date: datetime
    total_amount: float
    total_discount_amount: float = 0.0
    total_charge_amount: float = 0.0
    approved_by: Optional[UUID] = None
    customer_id: Optional[UUID] = None

class SaleCreate(SaleBase):
    details: List[SaleDetailCreate]

class SaleRead(SaleBase, BaseDTO):
    status: EntityStatus
    details: List[SaleDetailRead] = []
