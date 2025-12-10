"""StockMovement model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class StockMovement(Base):
    """Modelo de movimentação de estoque (auditoria)."""
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    movement_type = Column(String(50), nullable=False)  # entry, sale, transfer_out, transfer_in, adjustment_in, adjustment_out
    quantity = Column(Integer, nullable=False)
    movement_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    reference_id = Column(Integer, nullable=True)
    reference_type = Column(String(50), nullable=True)  # entry, distribution, sale, adjustment
    stock_before = Column(Integer, nullable=True)
    stock_after = Column(Integer, nullable=True)
    notes = Column(String(500), nullable=True)

    # Relationships
    product = relationship("Product")
    store = relationship("Store")
