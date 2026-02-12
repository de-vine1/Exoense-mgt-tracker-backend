from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from sqlalchemy import Column, JSON
from app.domain.enums.gender_type import Gender

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None

class BaseEntity(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_date: datetime = Field(default_factory=datetime.now)
    updated_date: datetime = Field(default_factory=datetime.now)

class Person(BaseEntity):
    first_name: str
    last_name: str
    date_of_birth: Optional[datetime] = None
    # Moved address to subclasses or use a way that prevents shared Column instance
    gender: Optional[Gender] = None
    email: str = Field(unique=True, index=True)
    phone_number: Optional[str] = None
    hashed_password: Optional[str] = Field(default=None)

    # We will define address in each inherited class to avoid SQLAlchemy "already assigned" error
