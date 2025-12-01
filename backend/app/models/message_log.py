# NEW FILE - Track all sent messages for history and debugging
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=True)

    # Recipient Info
    recipient_phone = Column(String(20), nullable=False)
    recipient_name = Column(String(255), nullable=True)

    # Message Details
    message_type = Column(String(50), nullable=False)  # text, image, document, catalog
    message_content = Column(Text, nullable=True)
    media_url = Column(Text, nullable=True)

    # WhatsApp API Response
    whatsapp_message_id = Column(String(255), nullable=True)
    status = Column(String(50), default="pending")  # pending, sent, delivered, read, failed
    error_message = Column(Text, nullable=True)
    api_response = Column(JSON, nullable=True)

    # Retry Logic
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    tenant = relationship("Tenant")
    call = relationship("Call")
