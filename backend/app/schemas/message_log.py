# NEW FILE - Schemas for message logs
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class MessageLogBase(BaseModel):
    recipient_phone: str
    recipient_name: Optional[str] = None
    message_type: str
    message_content: Optional[str] = None
    media_url: Optional[str] = None


class MessageLogCreate(MessageLogBase):
    tenant_id: int
    call_id: Optional[int] = None


class MessageLogUpdate(BaseModel):
    whatsapp_message_id: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None
    api_response: Optional[Any] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    retry_count: Optional[int] = None


class MessageLogResponse(MessageLogBase):
    id: int
    tenant_id: int
    call_id: Optional[int] = None
    whatsapp_message_id: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    retry_count: int
    created_at: datetime
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    class Config:
        from_attributes = True
