from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)

    is_active = Column(Boolean, nullable=False, server_default="true")
    setup_complete = Column(Boolean, nullable=False, server_default="false")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Users belonging to this tenant
    users = relationship(
        "User",
        back_populates="tenant",
        cascade="all, delete",
    )

    # Products / catalog entries
    products = relationship(
        "Product",
        back_populates="tenant",
        cascade="all, delete-orphan",
    )

    # One row of automation settings for this tenant
    automation_settings = relationship(
        "AutomationSettings",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete",
    )

    # Call history for this tenant
    calls = relationship(
        "Call",
        back_populates="tenant",
        cascade="all, delete",
    )

    webhook_calls = relationship("WebhookCall", back_populates="tenant")

    settings = relationship(
        "TenantSettings",
        back_populates="tenant",
        uselist=False,
        cascade="all, delete-orphan",
    )

