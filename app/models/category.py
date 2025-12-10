"""Category model."""
from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Category(Base):
    """Modelo de categoria de produtos."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
