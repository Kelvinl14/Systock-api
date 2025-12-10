"""Sale and SaleItem models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Sale(Base):
    """Modelo de venda."""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    sale_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    delivery_type = Column(String(50), nullable=True)
    tracking_code = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    predicted_delivery = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    total_value = Column(Float, nullable=True)

    # Relationships
    items = relationship("SaleItem", back_populates="sale")


class SaleItem(Base):
    """Modelo de item de venda."""
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=True)
    removed_at = Column(DateTime, nullable=True)

    # Relationships
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")
