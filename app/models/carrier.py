"""Carrier model."""
from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Carrier(Base):
    """Modelo de transportadora."""
    __tablename__ = "carriers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    cnpj = Column(String(20), unique=True, nullable=True)
    contact_info = Column(String(255), nullable=True)
