"""Sale schemas."""
from pydantic import BaseModel
from datetime import datetime


class SaleItemCreate(BaseModel):
    """Schema para criar item de venda."""
    product_id: int
    quantity: int
    unit_price: float
    total_price: float | None = None
    removed_at: datetime | None = None


class SaleCreate(BaseModel):
    """Schema para criar venda."""
    client_id: int
    store_id: int
    sale_date: datetime | None = None
    delivery_type: str | None = None
    tracking_code: str | None = None
    status: str = "pending"
    predicted_delivery: datetime | None = None
    delivered_at: datetime | None = None
    total_value: float | None = None
    items: list[SaleItemCreate]


class SaleItemRead(BaseModel):
    """Schema para ler item de venda."""
    id: int
    sale_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float | None = None
    removed_at: datetime | None = None

    class Config:
        from_attributes = True


class SaleRead(BaseModel):
    """Schema para ler venda."""
    id: int
    client_id: int
    store_id: int
    sale_date: datetime
    delivery_type: str | None = None
    tracking_code: str | None = None
    status: str
    predicted_delivery: datetime | None = None
    delivered_at: datetime | None = None
    total_value: float | None = None
    items: list[SaleItemRead] = []

    class Config:
        from_attributes = True
