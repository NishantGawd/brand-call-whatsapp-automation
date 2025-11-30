from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AutomationSettings(Base):
    __tablename__ = "automation_settings"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # each tenant has at most one settings row
        index=True,
    )

    # whether post-call WhatsApp automation is active
    enabled = Column(Boolean, nullable=False, server_default="false")

    # seconds after call ends before sending WhatsApp
    delay_seconds = Column(Integer, nullable=False, server_default="60")

    # minimum call duration in seconds required to trigger automation
    min_call_duration_seconds = Column(Integer, nullable=False, server_default="0")

    # send mode:
    # "thank_you_only",
    # "thank_you_and_full_catalog",
    # "thank_you_and_filtered_catalog"
    send_mode = Column(
        String(50),
        nullable=False,
        server_default="thank_you_and_full_catalog",
    )

    # simple CSV lists of category names for MVP
    include_categories = Column(String(500), nullable=True)
    exclude_categories = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    tenant = relationship("Tenant", back_populates="automation_settings")
