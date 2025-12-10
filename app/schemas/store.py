"""Store schemas."""
from pydantic import BaseModel


class StoreCreate(BaseModel):
    """Schema para criar loja."""
    name: str
    address: str | None = None


class StoreUpdate(BaseModel):
    """Schema para atualizar loja."""
    name: str | None = None
    address: str | None = None


class StoreRead(BaseModel):
    """Schema para ler loja."""
    id: int
    name: str
    address: str | None = None

    class Config:
        from_attributes = True
