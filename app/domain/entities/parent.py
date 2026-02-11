from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.entities.student import Student
    from app.domain.entities.wallet import Wallet

class Parent(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    firstname: str
    lastname: str
    email: str = Field(unique=True)
    hashed_password: str
    
    # One Parent -> Many Students
    children: List["Student"] = Relationship(back_populates="parent")
    
    # One Parent -> One Wallet
    wallet: Optional["Wallet"] = Relationship(
        sa_relationship_kwargs={"uselist": False}, 
        back_populates="parent"
    )
    
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)