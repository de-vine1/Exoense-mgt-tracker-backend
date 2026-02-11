from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domain.entities.parent import Parent
    from app.domain.entities.wallet import Wallet

class Student(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    reg_number: str = Field(unique=True, index=True)
    firstname: str
    lastname: str
    email: str = Field(unique=True)
    hashed_password: str
    
    grade: Optional[int] = Field(default=None)
    term: Optional[int] = Field(default=None)
    
    # Parent link is optional (allows self-registration)
    parent_id: Optional[UUID] = Field(default=None, foreign_key="parent.id")
    is_link_confirmed: bool = Field(default=False)
    
    # Relationships
    parent: Optional["Parent"] = Relationship(back_populates="children")
    wallet: Optional["Wallet"] = Relationship(
        sa_relationship_kwargs={"uselist": False}, 
        back_populates="student"
    )
    
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)