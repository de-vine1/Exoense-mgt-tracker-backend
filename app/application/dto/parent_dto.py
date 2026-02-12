from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.application.dto.base_dto import BaseDTO, AddressDTO
from app.domain.enums.gender_type import Gender
from app.domain.enums.entity_type import EntityStatus

class ParentBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[AddressDTO] = None
    occupation: Optional[str] = None

class ParentCreate(ParentBase):
    password: str

class ParentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[Gender] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[AddressDTO] = None
    occupation: Optional[str] = None
    status: Optional[EntityStatus] = None

class ParentRead(ParentBase, BaseDTO):
    status: EntityStatus
