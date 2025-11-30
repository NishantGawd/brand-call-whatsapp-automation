from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class WebhookCall(Base):
    __tablename__ = "webhook_calls"

    id = Column(Integer, primary_key=True, index=True)
    caller_number = Column(String, nullable=False)
    call_status = Column(String, nullable=False)
    call_duration_seconds = Column(Integer, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    # 🚀 Add this so relationships work correctly
    tenant = relationship("Tenant", back_populates="webhook_calls")
