from typing import Optional
from sqlmodel import Field
from app.domain.entities.base import Person, Address
from app.domain.enums.entity_type import EntityStatus
from sqlalchemy import Column, JSON

class Student(Person, table=True):
    address: Optional[Address] = Field(default=None, sa_column=Column(JSON))
    class_name: Optional[str] = None
    group_name: Optional[str] = None
    status: EntityStatus = Field(default=EntityStatus.ACTIVE)
    image: Optional[str] = None
    qr_code: Optional[str] = None
    reg_number: str = Field(unique=True, index=True)