from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class StudentBase(BaseModel):
    reg_number: str
    firstname: str
    lastname: str
    email: EmailStr
    grade: Optional[int] = None
    term: Optional[int] = None

class StudentCreate(StudentBase):
    password: str

class StudentResponse(StudentBase):
    id: UUID
    is_active: bool
    is_link_confirmed: bool
    parent_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

class StudentUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    grade: Optional[int] = None
    term: Optional[int] = None
    is_active: Optional[bool] = None
    is_link_confirmed: Optional[bool] = None
    parent_id: Optional[UUID] = None


class WalletResponse(BaseModel):
    balance: float
    payer_id: UUID
    payer_type: str
    
    class Config:
        from_attributes = True

