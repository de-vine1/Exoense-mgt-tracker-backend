from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class AdminBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
