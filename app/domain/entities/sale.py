from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlmodel import Field
from app.domain.entities.base import BaseEntity
from app.domain.enums.entity_type import EntityStatus

class Sale(BaseEntity, table=True):
    transaction_id: str = Field(unique=True, index=True)
    transaction_date: datetime = Field(default_factory=datetime.now)
    total_amount: float
    total_discount_amount: float = Field(default=0.0)
    total_charge_amount: float = Field(default=0.0)
    status: EntityStatus = Field(default=EntityStatus.PENDING)
    approved_by: Optional[UUID] = None
    customer_id: Optional[UUID] = None

class SaleDetail(BaseEntity, table=True):
    sale_id: UUID = Field(foreign_key="sale.id")
    product_name: str
    product_id: UUID = Field(foreign_key="product.id")
    amount: float
    discount_amount: float = Field(default=0.0)
    charge_amount: float = Field(default=0.0)
    quantity: int = Field(default=1)
