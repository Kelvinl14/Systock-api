"""Category schemas."""
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """Schema para criar categoria."""
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    """Schema para atualizar categoria."""
    name: str | None = None
    description: str | None = None


class CategoryRead(BaseModel):
    """Schema para ler categoria."""
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True
