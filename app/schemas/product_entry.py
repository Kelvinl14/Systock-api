"""ProductEntry schemas."""
from pydantic import BaseModel
from datetime import datetime


class ProductEntryItemCreate(BaseModel):
    """Schema para criar item de entrada."""
    product_id: int
    quantity: int
    unit_price: float
    total_price: float | None = None
    lot_number: str | None = None
    expiration_date: datetime | None = None
    received_at: datetime | None = None


class ProductEntryCreate(BaseModel):
    """Schema para criar entrada de produtos."""
    supplier_id: int
    entry_date: datetime | None = None
    invoice_number: str | None = None
    total_value: float | None = None
    status: str = "pending"
    items: list[ProductEntryItemCreate]


class ProductEntryItemRead(BaseModel):
    """Schema para ler item de entrada."""
    id: int
    product_entry_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float | None = None
    lot_number: str | None = None
    expiration_date: datetime | None = None
    received_at: datetime | None = None

    class Config:
        from_attributes = True


class ProductEntryRead(BaseModel):
    """Schema para ler entrada de produtos."""
    id: int
    supplier_id: int
    entry_date: datetime
    invoice_number: str | None = None
    total_value: float | None = None
    status: str
    items: list[ProductEntryItemRead] = []

    class Config:
        from_attributes = True
