# app/models/product.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    gender = Column(String(50), nullable=True, index=True)
    tags = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    tenant = relationship("Tenant", back_populates="products")
