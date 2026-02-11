from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.entities.student import Student
    from app.domain.entities.parent import Parent

class Wallet(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    balance: Decimal = Field(default=Decimal("0.0"), decimal_places=2)
    
    # Foreign Keys
    student_id: Optional[UUID] = Field(default=None, foreign_key="student.id")
    parent_id: Optional[UUID] = Field(default=None, foreign_key="parent.id")
    
    # Relationships
    student: Optional["Student"] = Relationship(back_populates="wallet")
    parent: Optional["Parent"] = Relationship(back_populates="wallet")