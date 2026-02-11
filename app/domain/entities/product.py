from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.entities.fee_category import FeeCategory

class Fee(SQLModel, table=True):
    __tablename__ = "fee"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    amount: Decimal = Field(decimal_places=2)
    
    category_id: UUID = Field(foreign_key="fee_category.id")
    category: "FeeCategory" = Relationship(back_populates="fees")
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)