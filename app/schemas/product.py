"""Product schemas."""
from pydantic import BaseModel
from datetime import date


class ProductCreate(BaseModel):
    """Schema para criar produto."""
    name: str
    description: str | None = None
    cost_price: float
    sale_price: float
    date_added: date | None = None
    active: bool = True
    category_id: int | None = None


class ProductUpdate(BaseModel):
    """Schema para atualizar produto."""
    name: str | None = None
    description: str | None = None
    cost_price: float | None = None
    sale_price: float | None = None
    active: bool | None = None
    category_id: int | None = None


class ProductRead(BaseModel):
    """Schema para ler produto."""
    id: int
    name: str
    description: str | None = None
    cost_price: float
    sale_price: float
    date_added: date | None = None
    active: bool
    category_id: int | None = None

    class Config:
        from_attributes = True
