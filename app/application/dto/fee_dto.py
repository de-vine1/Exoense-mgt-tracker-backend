from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional

class FeeCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class FeeCategoryResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class FeeCreate(BaseModel):
    name: str
    amount: Decimal
    category_id: UUID

class FeeResponse(BaseModel):
    id: UUID
    name: str
    amount: Decimal
    category_id: UUID
    is_active: bool

    class Config:
        from_attributes = True

class StudentFeeResponse(BaseModel):
    id: UUID
    student_id: UUID
    fee_id: UUID
    amount_due: Decimal
    amount_paid: Decimal
    is_paid: bool
    assigned_at: datetime
    paid_at: Optional[datetime] = None

    class Config:
        from_attributes = True
