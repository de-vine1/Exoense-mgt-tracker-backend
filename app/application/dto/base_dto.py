from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class AddressDTO(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None

class BaseDTO(BaseModel):
    id: UUID
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True
