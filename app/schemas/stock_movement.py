"""StockMovement schemas."""
from pydantic import BaseModel
from datetime import datetime


class StockMovementCreate(BaseModel):
    """Schema para criar movimentação de estoque."""
    product_id: int
    store_id: int
    movement_type: str
    quantity: int
    movement_date: datetime | None = None
    reference_id: int | None = None
    reference_type: str | None = None
    stock_before: int | None = None
    stock_after: int | None = None
    notes: str | None = None


class StockMovementRead(BaseModel):
    """Schema para ler movimentação de estoque."""
    id: int
    product_id: int
    store_id: int
    movement_type: str
    quantity: int
    movement_date: datetime
    reference_id: int | None = None
    reference_type: str | None = None
    stock_before: int | None = None
    stock_after: int | None = None
    notes: str | None = None

    class Config:
        from_attributes = True
