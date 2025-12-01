# NEW FILE - Schemas for tenant settings
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TenantSettingsBase(BaseModel):
    thank_you_message: Optional[str] = "Thank you for calling! Here's our latest catalog:"
    include_catalog: Optional[bool] = True
    catalog_header_message: Optional[str] = "Browse our exclusive collection:"
    catalog_footer_message: Optional[str] = "Reply with product number to inquire!"
    message_delay_seconds: Optional[int] = Field(default=5, ge=0, le=300)


class TenantSettingsCreate(TenantSettingsBase):
    tenant_id: int


class TenantSettingsUpdate(TenantSettingsBase):
    pass


class WhatsAppCredentialsUpdate(BaseModel):
    whatsapp_phone_number_id: str
    whatsapp_business_account_id: str
    whatsapp_access_token: str
    whatsapp_webhook_verify_token: Optional[str] = None


class WebhookSecurityUpdate(BaseModel):
    webhook_secret_key: str


class TenantSettingsResponse(TenantSettingsBase):
    id: int
    tenant_id: int
    whatsapp_phone_number_id: Optional[str] = None
    whatsapp_business_account_id: Optional[str] = None
    is_whatsapp_configured: bool = False
    webhook_secret_key: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TenantSettingsPublic(BaseModel):
    """Public response - hides sensitive credentials"""
    id: int
    tenant_id: int
    thank_you_message: str
    include_catalog: bool
    catalog_header_message: str
    catalog_footer_message: str
    message_delay_seconds: int
    is_whatsapp_configured: bool
    has_webhook_secret: bool = False
    is_active: bool

    class Config:
        from_attributes = True
