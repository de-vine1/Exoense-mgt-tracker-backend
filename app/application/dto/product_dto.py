from typing import Optional
from pydantic import BaseModel
from app.application.dto.base_dto import BaseDTO
from app.domain.enums.entity_type import EntityStatus

class ProductBase(BaseModel):
    name: str
    code: str
    measure_unit: Optional[str] = None
    image: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    measure_unit: Optional[str] = None
    image: Optional[str] = None
    price: Optional[float] = None
    status: Optional[EntityStatus] = None

class ProductRead(ProductBase, BaseDTO):
    status: EntityStatus
