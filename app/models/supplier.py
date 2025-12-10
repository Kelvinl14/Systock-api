"""Supplier model."""
from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Supplier(Base):
    """Modelo de fornecedor."""
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    cnpj = Column(String(20), unique=True, nullable=False)
    contact_info = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
