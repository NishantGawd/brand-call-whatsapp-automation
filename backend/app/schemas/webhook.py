# COMPLETE REWRITE - Proper webhook schemas for different providers
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


# Generic webhook payload
class GenericWebhookPayload(BaseModel):
    provider: Optional[str] = None
    raw_data: Optional[Any] = None


# Twilio webhook payload
class TwilioCallWebhook(BaseModel):
    CallSid: str
    AccountSid: str
    From_: str = Field(alias="From")
    To: str
    CallStatus: str  # queued, ringing, in-progress, completed, busy, failed, no-answer
    Direction: str  # inbound, outbound
    CallerName: Optional[str] = None
    CallDuration: Optional[int] = None
    Timestamp: Optional[str] = None

    class Config:
        populate_by_name = True


# Exotel webhook payload
class ExotelCallWebhook(BaseModel):
    CallSid: str
    From_: str = Field(alias="From")
    To: str
    Status: str  # ringing, in-progress, completed, failed, busy, no-answer
    Direction: str
    RecordingUrl: Optional[str] = None
    CurrentTime: Optional[str] = None
    DialCallDuration: Optional[int] = None

    class Config:
        populate_by_name = True


# Generic call ended event (normalized)
class CallEndedEvent(BaseModel):
    call_sid: str
    caller_phone: str
    receiver_phone: str
    status: str
    duration_seconds: Optional[int] = None
    provider: str  # twilio, exotel, generic
    raw_payload: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Webhook response
class WebhookResponse(BaseModel):
    success: bool
    message: str
    call_id: Optional[int] = None
    automation_triggered: bool = False
