"""Product model."""
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Product(Base):
    """Modelo de produto."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    cost_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    date_added = Column(Date, nullable=True)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationships
    category = relationship("Category")
