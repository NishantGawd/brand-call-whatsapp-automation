from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class TenantSettings(Base):
    __tablename__ = "tenant_settings"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    enabled = Column(Boolean, default=True)
    min_call_duration_seconds = Column(Integer, default=0)

    tenant = relationship("Tenant", back_populates="settings")
