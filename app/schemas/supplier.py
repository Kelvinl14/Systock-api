"""Supplier schemas."""
from pydantic import BaseModel


class SupplierCreate(BaseModel):
    """Schema para criar fornecedor."""
    name: str
    cnpj: str
    contact_info: str | None = None
    address: str | None = None


class SupplierUpdate(BaseModel):
    """Schema para atualizar fornecedor."""
    name: str | None = None
    contact_info: str | None = None
    address: str | None = None


class SupplierRead(BaseModel):
    """Schema para ler fornecedor."""
    id: int
    name: str
    cnpj: str
    contact_info: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True
