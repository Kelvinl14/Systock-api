"""ProductEntry and ProductEntryItem models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class ProductEntry(Base):
    """Modelo de entrada de produtos (compra)."""
    __tablename__ = "product_entries"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    entry_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    invoice_number = Column(String(50), nullable=True)
    total_value = Column(Float, nullable=True)
    status = Column(String(50), nullable=False, default="pending")

    # Relationships
    supplier = relationship("Supplier")
    items = relationship("ProductEntryItem", back_populates="entry")


class ProductEntryItem(Base):
    """Modelo de item de entrada de produtos."""
    __tablename__ = "product_entry_items"

    id = Column(Integer, primary_key=True, index=True)
    product_entry_id = Column(Integer, ForeignKey("product_entries.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=True)
    lot_number = Column(String(50), nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    received_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    # Relationships
    entry = relationship("ProductEntry", back_populates="items")
    product = relationship("Product")
