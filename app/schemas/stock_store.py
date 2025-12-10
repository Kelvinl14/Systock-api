"""StockStore schemas."""
from pydantic import BaseModel
from datetime import datetime


class StockStoreCreate(BaseModel):
    """Schema para criar estoque por loja."""
    store_id: int
    product_id: int
    quantity: int


class StockStoreUpdate(BaseModel):
    """Schema para atualizar estoque por loja."""
    quantity: int | None = None


class StockStoreRead(BaseModel):
    """Schema para ler estoque por loja."""
    id: int
    store_id: int
    product_id: int
    quantity: int
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
