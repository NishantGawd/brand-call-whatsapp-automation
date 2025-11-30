from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # "inbound" or "outbound"
    direction = Column(String(20), nullable=False)

    # raw phone numbers as strings
    from_number = Column(String(50), nullable=False)
    to_number = Column(String(50), nullable=False)

    # normalized customer number (the non-dealer party)
    customer_number = Column(String(50), nullable=False, index=True)

    # e.g. "completed", "no-answer", "busy", "failed"
    status = Column(String(50), nullable=False)

    # provider info
    provider = Column(String(50), nullable=True)
    provider_call_id = Column(String(100), nullable=True, index=True)

    # timing info
    duration_seconds = Column(Integer, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # raw payload from provider as JSON string
    raw_payload = Column(Text, nullable=True)

    # whether this call qualifies for automation (according to settings)
    should_trigger_automation = Column(
        Boolean, nullable=False, server_default="false"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    tenant = relationship("Tenant", back_populates="calls")
