from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

class FeeCategory(SQLModel, table=True):
    __tablename__ = "fee_category"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    fees: list["Fee"] = Relationship(back_populates="category")
    
    created_at: datetime = Field(default_factory=datetime.now)
