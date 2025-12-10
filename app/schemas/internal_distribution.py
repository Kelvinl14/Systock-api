"""InternalDistribution schemas."""
from pydantic import BaseModel
from datetime import datetime


class InternalDistributionItemCreate(BaseModel):
    """Schema para criar item de distribuição interna."""
    product_id: int
    quantity: int
    registered_at: datetime | None = None


class InternalDistributionCreate(BaseModel):
    """Schema para criar distribuição interna."""
    from_store_id: int
    to_store_id: int
    distribution_date: datetime | None = None
    status: str = "pending"
    items: list[InternalDistributionItemCreate]


class InternalDistributionItemRead(BaseModel):
    """Schema para ler item de distribuição interna."""
    id: int
    internal_distribution_id: int
    product_id: int
    quantity: int
    registered_at: datetime | None = None

    class Config:
        from_attributes = True


class InternalDistributionRead(BaseModel):
    """Schema para ler distribuição interna."""
    id: int
    from_store_id: int
    to_store_id: int
    distribution_date: datetime
    status: str
    items: list[InternalDistributionItemRead] = []

    class Config:
        from_attributes = True
