"""Client model."""
from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Client(Base):
    """Modelo de cliente."""
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
