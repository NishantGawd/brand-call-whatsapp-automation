from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CallBase(BaseModel):
    direction: str = Field(..., description="'inbound' or 'outbound'")
    from_number: str
    to_number: str
    customer_number: str
    status: str
    provider: Optional[str] = None
    provider_call_id: Optional[str] = None
    duration_seconds: Optional[int] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class CallWebhookIn(CallBase):
    """
    Payload we expect from telephony webhook (normalized for now).
    Later we can add provider-specific adapters.
    """

    raw_payload: Optional[dict] = Field(
        default=None, description="Original payload from provider"
    )


class CallOut(CallBase):
    id: int
    tenant_id: int
    should_trigger_automation: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
