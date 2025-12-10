"""Store model."""
from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Store(Base):
    """Modelo de loja."""
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    address = Column(String(500), nullable=True)
