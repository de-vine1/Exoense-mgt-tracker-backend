from typing import Optional
from sqlmodel import Field
from app.domain.entities.base import Person, Address
from app.domain.enums.transaction_type import EntityStatus
from sqlalchemy import Column, JSON

class Parent(Person, table=True):
    address: Optional[Address] = Field(default=None, sa_column=Column(JSON))
    occupation: Optional[str] = None
    status: EntityStatus = Field(default=EntityStatus.ACTIVE)