"""Carrier schemas."""
from pydantic import BaseModel


class CarrierCreate(BaseModel):
    """Schema para criar transportadora."""
    name: str
    cnpj: str | None = None
    contact_info: str | None = None


class CarrierUpdate(BaseModel):
    """Schema para atualizar transportadora."""
    name: str | None = None
    contact_info: str | None = None


class CarrierRead(BaseModel):
    """Schema para ler transportadora."""
    id: int
    name: str
    cnpj: str | None = None
    contact_info: str | None = None

    class Config:
        from_attributes = True
