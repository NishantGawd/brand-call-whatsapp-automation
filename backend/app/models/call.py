# Updated with automation tracking fields
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    # Call Details
    call_sid = Column(String(255), index=True, nullable=True)
    caller_phone = Column(String(20), nullable=False, index=True)
    receiver_phone = Column(String(20), nullable=True)

    # Status and Duration
    status = Column(String(50), default="completed")  # completed, busy, no-answer, failed
    duration_seconds = Column(Integer, nullable=True)

    # Provider Info
    provider = Column(String(50), default="generic")  # twilio, exotel, generic

    # Automation Tracking
    automation_triggered = Column(Boolean, default=False)
    automation_triggered_at = Column(DateTime(timezone=True), nullable=True)
    automation_status = Column(String(50), nullable=True)  # pending, sent, failed

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="calls")
