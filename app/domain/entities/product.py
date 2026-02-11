from typing import Optional
from sqlmodel import Field
from app.domain.entities.base import BaseEntity
from app.domain.enums.entity_type import EntityStatus

class Product(BaseEntity, table=True):
    name: str = Field(index=True)
    code: str = Field(unique=True, index=True)
    measure_unit: Optional[str] = None
    image: Optional[str] = None
    price: float
    status: EntityStatus = Field(default=EntityStatus.ACTIVE)
