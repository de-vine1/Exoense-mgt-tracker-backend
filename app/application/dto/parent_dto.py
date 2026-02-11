from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class ParentBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

class ParentCreate(ParentBase):
    password: str

class ParentResponse(ParentBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ParentUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

