from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class AdminBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class AdminResponse(AdminBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

