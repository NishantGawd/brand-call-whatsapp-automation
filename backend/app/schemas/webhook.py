# app/schemas/webhook.py
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel

class WebhookCallRequest(BaseModel):
    direction: str
    from_number: str
    to_number: str
    customer_number: str
    status: str
    provider: str
    provider_call_id: str
    duration_seconds: int
    started_at: datetime
    ended_at: datetime
    raw_payload: Optional[dict[str, Any]] = None
