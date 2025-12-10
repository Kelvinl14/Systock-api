"""Client schemas."""
from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    """Schema para criar cliente."""
    name: str
    cpf_cnpj: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None


class ClientUpdate(BaseModel):
    """Schema para atualizar cliente."""
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None


class ClientRead(BaseModel):
    """Schema para ler cliente."""
    id: int
    name: str
    cpf_cnpj: str
    email: str
    phone: str | None = None
    address: str | None = None

    class Config:
        from_attributes = True
