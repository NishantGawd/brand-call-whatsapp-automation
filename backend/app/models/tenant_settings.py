# COMPLETE REWRITE - Adding WhatsApp credentials and message customization
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class TenantSettings(Base):
    __tablename__ = "tenant_settings"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), unique=True, nullable=False)

    # WhatsApp Cloud API Credentials
    whatsapp_phone_number_id = Column(String(100), nullable=True)
    whatsapp_business_account_id = Column(String(100), nullable=True)
    whatsapp_access_token = Column(Text, nullable=True)  # Encrypted in production
    whatsapp_webhook_verify_token = Column(String(255), nullable=True)

    # Webhook Security (for Twilio/Exotel)
    webhook_secret_key = Column(String(255), nullable=True)  # Secret to verify incoming webhooks

    # Message Customization
    thank_you_message = Column(Text, default="Thank you for calling! Here's our latest catalog:")
    include_catalog = Column(Boolean, default=True)
    catalog_header_message = Column(Text, default="Browse our exclusive collection:")
    catalog_footer_message = Column(Text, default="Reply with product number to inquire!")

    # Timing Settings
    message_delay_seconds = Column(Integer, default=5)  # Delay before sending after call ends

    # Status
    is_whatsapp_configured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    tenant = relationship("Tenant", back_populates="settings")
