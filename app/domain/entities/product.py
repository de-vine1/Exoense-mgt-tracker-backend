from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.entities.category import Category

class Product(SQLModel, table=True):
    __tablename__ = "product"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    amount: Decimal = Field(decimal_places=2)
    
    category_id: UUID = Field(foreign_key="category.id")
    category: "Category" = Relationship(back_populates="products")
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)