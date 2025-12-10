"""InternalDistribution and InternalDistributionItem models."""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class InternalDistribution(Base):
    """Modelo de distribuição interna entre lojas."""
    __tablename__ = "internal_distributions"

    id = Column(Integer, primary_key=True, index=True)
    from_store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    to_store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    distribution_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(50), nullable=False, default="pending")

    # Relationships
    items = relationship("InternalDistributionItem", back_populates="distribution")


class InternalDistributionItem(Base):
    """Modelo de item de distribuição interna."""
    __tablename__ = "internal_distribution_items"

    id = Column(Integer, primary_key=True, index=True)
    internal_distribution_id = Column(Integer, ForeignKey("internal_distributions.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    registered_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    # Relationships
    distribution = relationship("InternalDistribution", back_populates="items")
    product = relationship("Product")
