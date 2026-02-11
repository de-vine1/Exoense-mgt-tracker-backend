from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.entities.product import Product

class Category(SQLModel, table=True):
    __tablename__ = "category"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    # One Category -> Many Products
    products: List["Product"] = Relationship(back_populates="category")
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.now)
