from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.entities.student import Student
    from app.domain.entities.fee import Fee

class StudentFee(SQLModel, table=True):
    __tablename__ = "student_fee"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    student_id: UUID = Field(foreign_key="student.id")
    fee_id: UUID = Field(foreign_key="fee.id")
    
    amount_due: Decimal = Field(decimal_places=2)
    amount_paid: Decimal = Field(default=Decimal("0.0"), decimal_places=2)
    is_paid: bool = Field(default=False)
    
    assigned_at: datetime = Field(default_factory=datetime.now)
    paid_at: Optional[datetime] = Field(default=None)
    
    # Relationships
    student: "Student" = Relationship()
    fee: "Fee" = Relationship()
