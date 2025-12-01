# Updated to include settings relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)

    # Business Info
    business_name = Column(String(255), nullable=True)
    business_phone = Column(String(20), nullable=True)
    business_email = Column(String(255), nullable=True)
    business_address = Column(String(500), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_setup_complete = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="tenant")
    products = relationship("Product", back_populates="tenant")
    calls = relationship("Call", back_populates="tenant")
    settings = relationship("TenantSettings", back_populates="tenant", uselist=False)
    automation_settings = relationship("AutomationSettings", back_populates="tenant", uselist=False)
