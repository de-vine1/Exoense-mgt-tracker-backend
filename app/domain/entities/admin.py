from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

class Admin(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    firstname: str
    lastname: str
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
